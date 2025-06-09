import xml.etree.ElementTree as ET
import pandas as pd
from utils.ordered_name import *  # NOQA
import os
from utils.download_handler import *  # NOQA
from pathlib import Path
import numpy as np
from collections import defaultdict
import math


def xbrl_to_df(instance_path):
    print(f"Reading {instance_path}...")
    tree = ET.parse(instance_path)
    root = tree.getroot()

    facts = {}
    for idx, elem in enumerate(root.iter()):
        if not elem.attrib:  # Skip elements with no attributes
            continue

        context_ref = elem.attrib.get('contextRef')
        if context_ref:
            # print(f"\n=== Processing Element Index: {idx} ===")
            tag_name = elem.tag.split('}')[-1]
            value = elem.text.strip() if elem.text else None

            # Print debug info
            # print(f"Tag Name: {tag_name}")
            # print(f"Value: {value}")
            # print("All Attributes:")
            # for attr, val in elem.attrib.items():
            #    print(f"  {attr}: {val}")

            # Store in facts
            fact_key = f"{tag_name}_{context_ref}"
            facts[fact_key] = {
                'value': value,
                'context': context_ref,
                'name': tag_name,
                # Capture all attributes explicitly
                'id': elem.attrib.get('id'),
                'unitRef': elem.attrib.get('unitRef'),
                'decimals': elem.attrib.get('decimals'),
                'precision': elem.attrib.get('precision'),
                # Or capture all attributes dynamically
                # 'all_attributes': dict(elem.attrib)  # Optional
            }

    df = pd.DataFrame(facts).T
    return (df)


def preprocess_raw_df(raw_df: pd.DataFrame, period: str = "All",
                      schema_mapping: pd.DataFrame = None):
    df = raw_df.copy()

    if period == "Prior":
        year_end = df[df.name == 'PriorPeriodEndDate'].reset_index(drop=True)\
            .get("value")[0]

        df['year'] = year_end
    else:
        try:
            prior2_year_end = df[df.name == 'Prior2YearEndDate'].reset_index(
                drop=True) .get("value")[0]
        except Exception as e:
            print("2 Year Prior not found..")
            prior2_year_end = None
        prior_year_end = df[df.name == 'PriorPeriodEndDate'].reset_index(
            drop=True) .get("value")[0]
        year_end = df[df.name == 'CurrentPeriodEndDate'].reset_index(
            drop=True) .get("value")[0]
        df.loc[df.context.str.contains("Prior2"), "year"] = prior2_year_end
        df.loc[df.context.str.contains(
            "PriorYear|PriorEnd"), "year"] = prior_year_end
        df.loc[df.context.str.contains("CurrentYear"), "year"] = year_end

    # df['year'] = year_end

    if any(
        year in year_end for year in [
            '2018',
            '2019',
            '2020',
            '2021',
            '2022',
            '2023']) and schema_mapping is not None:
        print("Old schema.. joining with the mapping df")
        df = pd.merge(df, schema_mapping, how='left', on='name')
        # print(df['processed_id'])
    else:
        df['processed_id'] = df['id'].apply(lambda x: x.split('_')[0])

    if period == "Current":
        df = df[df.context.str.contains('Current')]
    elif period == "Prior":
        cond1 = df.context.str.contains('Prior', na=False)
        cond2 = df.processed_id.astype(str).str.contains('1000000', na=False)
        df = df[cond1 | cond2]
    else:
        df = df

    # industry = df[df.name == 'EntityMainIndustry'].reset_index(drop = True)\
    # .get("value")[0]

    return df


def normalize_multiplier_value(row, convert_billion_idr=None,
                               convert_million_usd=None):
    # print(f"Normalizing {row['value']}...")

    try:
        value = np.float64(row['value'])
    except Exception as E:
        # print(E)
        return row['value']

    if pd.isna(row['value']):
        # print("Value is NaN")
        return row['value']

    try:
        unit = row['unitRef'].lower()
    except Exception as E:
        # print(f"No unit: {E}")
        return value

    if "pershares" in unit:
        # value = np.float64(row['value'])
        return value
    else:
        try:
            decimals = int(row['decimals'])
        except Exception as E:
            # print(f"No decimals: {E}")
            return value

        if decimals < 0:
            multiplier = -1 * decimals
        else:
            multiplier = decimals

        # print(f"Multiplier is 10^{multiplier}. Normalizing value...")

        currency = row['unitRef']
        # print(f"Currency is {currency}")
        if currency == "IDR":
            if convert_billion_idr:
                if multiplier == 6 or multiplier == 0:
                    value = value / 10**9
                else:
                    # print("9")
                    value = value / 10**9
            else:
                value = value / 10**multiplier

            return value
        else:
            if convert_million_usd:
                if multiplier == 3 or multiplier == 0:
                    value = value / 10**6
                elif multiplier == 6:
                    # print("9")
                    value = value / 10**6
            else:
                value = value / 10**multiplier
            return value


def download_and_combine_xbrl(stock_code, years, quarterly):
    print(f"Downloading {stock_code} report for {years}...")
    urls = []
    filenames = []
    quarter_list = ['Q1', 'Q2', 'Q3', 'FY']

    directory = f"./data/{stock_code}"
    # directory_exist = os.path.isdir('directory')
    Path(directory).mkdir(parents=True, exist_ok=True)

    for year in years:
        if quarterly:
            url = [
                generate_url(  # NOQA
                    symbol=stock_code,
                    year=year,
                    period=p) for p in quarter_list]

            for u in url:
                urls.append(u)

            filename = [
                generate_filename(  # NOQA
                    symbol=stock_code,
                    year=year,
                    period=p) for p in quarter_list]
            for file in filename:
                filenames.append(file)

        else:
            url = generate_url(stock_code, year=year, period="FY")  # NOQA
            urls.append(url)

            filename = generate_filename(stock_code, year=year, period="FY")  # NOQA
            filenames.append(filename)

    instance_paths = [f"{filename}/instance.xbrl" for filename in filenames]

    i = 0
    while i < len(filenames):
        # print(i)
        url = urls[i]
        filename = filenames[i]

        if os.path.exists(instance_paths[i]):
            print(f"[PASS] {filename} File Already Exists..")
            i += 1
        else:
            download_succeeded = download_zip_file(url=url, filename=filename)  # NOQA

            if not download_succeeded:
                # print("False")
                # Remove failed item from BOTH lists to maintain alignment
                filenames.pop(i)
                instance_paths.pop(i)
                urls.pop(i)
                # Do NOT increment i here since next item shifts to current
                # index
            else:
                i += 1

    preprocessed_dfs = []

    latest_raw_df = xbrl_to_df(instance_paths[-1])
    latest_processed_df = preprocess_raw_df(raw_df=latest_raw_df,
                                            period="Current")
    name_id_mapping = latest_processed_df[['name', 'processed_id']]\
        .reset_index(drop=True).drop_duplicates()

    for path in instance_paths:
        raw_df = xbrl_to_df(path)
        preprocessed_df = preprocess_raw_df(raw_df=raw_df,
                                            schema_mapping=name_id_mapping,
                                            period="All")

        preprocessed_dfs.append(preprocessed_df)

    combined_df = pd.concat(
        [df for df in preprocessed_dfs]).reset_index(drop=True)
    return combined_df


def convert_cumulative_to_quarterly(df):
    """
    Convert cumulative quarterly values to actual quarterly values,
    handling non-numeric data and missing first quarters correctly.

    - If a value is not numeric, the original value is kept.
    - If a quarter's data is missing, the next quarter's value will be NaN.
    - Specifically handles cases where the first quarter of a year is missing.

    Args:
        df: DataFrame with identifier columns and date columns.

    Returns:
        DataFrame with corrected quarterly values.
    """
    # Use a copy to avoid modifying the original DataFrame
    result_df = df.copy()

    # Identify identifier columns and date columns
    id_cols = ['name', 'formatted_name']
    id_vars = [col for col in id_cols if col in df.columns]
    date_cols = sorted(
        [col for col in df.columns if col not in id_vars],
        key=lambda x: pd.to_datetime(x, errors='coerce')
    )

    # Set index for easier row-wise operations
    if id_vars:
        result_df = result_df.set_index(id_vars)
        df_indexed = df.set_index(id_vars)
    else:
        df_indexed = df

    # Group date columns by year
    dates_by_year = defaultdict(list)
    for date_col in date_cols:
        try:
            year = pd.to_datetime(date_col).year
            dates_by_year[year].append(date_col)
        except (ValueError, TypeError):
            # Ignore columns that can't be parsed as dates
            continue

    # Process the data for each year separately
    for year, cols in dates_by_year.items():
        if not cols:
            continue

        original_yearly_data = df_indexed[cols]
        numeric_yearly_data = original_yearly_data.apply(pd.to_numeric, errors='coerce')

        previous_quarter_cumulative = numeric_yearly_data.shift(periods=1, axis=1)
        quarterly_data = numeric_yearly_data - previous_quarter_cumulative

        # *** THE FIX IS HERE ***
        # Only restore the first column's value if it IS the actual first quarter.
        # If the first available column is Q2, its value should remain NaN
        # because Q2_cumulative - (missing Q1) = NaN.
        first_col_date = pd.to_datetime(cols[0])
        if first_col_date.quarter == 1:
            quarterly_data[cols[0]] = numeric_yearly_data[cols[0]]

        # Restore original non-numeric values
        final_yearly_data = quarterly_data.where(
            original_yearly_data.isna() | numeric_yearly_data.notna(),
            original_yearly_data
        )

        result_df[cols] = final_yearly_data

    return result_df.reset_index()

def get_id_availability(df: pd.DataFrame, 
                        main_industry: str):
    
    general_mapping_list = ['1210000', '1311000', '1321000', '1312000',
                        '1510000', '1610000', 
                        '1630000', '1632000', '1620100', '1620200',
                        '1640300', '1620500', '1620400', '1620300', 
                        '1640100', '1640200',
                        '1640300', '1691000a', '1691100', '1692000',
                        '1693000', '1696000', '1693100', '1616000',
                        '1617000', '1618000', '1619000', '1670000',
                        '1671000']
    
    finance_mapping_list = ['4220000', '4312000', '4322000', '4510000',
                        '4610000', '4611100a', '4612100a', '4613100a',
                        '4614100', '4622100', '4621100', '4623100',
                        '4624100', '4631100', '4632100']
    
    unique_id = df.processed_id.unique()
    unique_id = set(unique_id)
    unique_id = {x for x in unique_id if not (isinstance(x, float) and math.isnan(x))}

    id_availability_dict = {}

    if "General" in main_industry:
        mapping_list = general_mapping_list
    elif "Financial" in main_industry:
        mapping_list = finance_mapping_list
    else:
        print(f"Currently {main_industry} is not supported")
        return None

    for s in mapping_list:
    # Check if any element in unique_id CONTAINS the string s
    # We need to handle potential non-string types in unique_id, like float('nan')
        is_available = any(s in item for item in unique_id if isinstance(item, str))
        id_availability_dict[s] = is_available
    
    return id_availability_dict


def get_general_financial_table(
    combined_df: pd.DataFrame,
    name_mapping_path: str,
    table_type: str,
    convert_billion_idr: bool = True,
    convert_million_usd: bool = True
) -> pd.DataFrame:
    """Generate standardized financial tables with consistent normalization"""
    config = {
        'general_info': {
            'id_filter': "1000000",
            'ordered_names': ORDERED_GI_NAME,
            'additional_filters': None,
            'drop_cols': ['id', 'unitRef', 'precision'],
            'msg': "General Info"
        },
        'balance_sheet': {
            'id_filter': ["1210000", "1612000"],
            'ordered_names': ORDERED_GENERAL_BS_NAME,
            'additional_filters': lambda df: (
                df.name.isin([
                    "PropertyPlantAndEquipment", "PropertyAndEquipment",
                    'CurrentRealEstateAssets', 'NonCurrentRealEstateAssets', 'CurrentInventories',
                    'NonCurrentInventories', 'ShortTermBankLoans', 'LongTermBankLoans',
                    'LongTermBondsPayable',
                    'CurrentMaturitiesOfBankLoans', 'CurrentMaturitiesOfBondsPayable'
                ]) &
                df.context.isin(["PriorEndYearInstant", "CurrentYearInstant"])
            ),
            'preprocess': lambda df: df.assign(
                processed_id='IXF1210000E02',
                # name=df['name'].str.replace('PropertyAndEquipment', 'PropertyPlantAndEquipment')
            ),
            'msg': "Balance Sheet"
        },
        'income_statement': {
            'id_filter': ["1321000", "1311000", "1312000"],
            'ordered_names': ORDERED_GENERAL_IS_NAME,
            'additional_filters': lambda df: (
                df.name.isin([
                    "SalesAndRevenue", "CostOfSalesAndRevenue",
                    "FinanceCosts",
                    'UnrealisedGainsLossesOnChangesInFairValueOfAvailableForSaleFinancialAssetsBeforeTax'
                ]) &
                df.context.isin(["PriorYearDuration", "CurrentYearDuration"])
            ),
            'preprocess': lambda df: df.assign(
                # processed_id='IXF1210000E02',
                name=df['name'].str.replace(
                    r'\bFinanceCosts\b',
                    'InterestAndFinanceCosts',
                    regex=True
                ).str.replace(
                    r'\bUnrealisedGainsLossesOnChangesInFairValueOfAvailableForSaleFinancialAssetsBeforeTax\b',
                    'UnrealisedGainsLossesOnChangesInFairValueThroughOtherComprehensiveIncomeFinancialAssetsBeforeTax',
                    regex=True
                )
            ),
            'msg': "Income Statement"
        },
        'cash_flow': {
            'id_filter': "1510000",
            'ordered_names': ORDERED_GENERAL_CF_NAME,
            'additional_filters': lambda df: (
                df.name.isin([
                    "WithdrawalPlacementOfFinancialAssetsAvailableForSale"
                ]) &
                df.context.isin(["PriorYearDuration", "CurrentYearDuration"])
            ),
            'preprocess': lambda df: df.assign(
                # processed_id='IXF1210000E02',
                name=df['name'].str.replace(
                    r'\bWithdrawalPlacementOfFinancialAssetsAvailableForSale\b',
                    'WithdrawalPlacementOfFinancialAssetsFairValueThroughOtherComprehensiveIncome',
                    regex=True
                )
            ),
            'msg': "Cash Flow"
        },
        'accounting_policies': {
            'id_filter': "1610000",
            'ordered_names': ORDERED_GENERAL_AP_NAME,
            'additional_filters': None,
            'drop_cols': ['id', 'unitRef', 'precision'],
            'msg': "Accounting Policies"
        },
        'inventory_breakdown': {
            'id_filter': "1630000",
            'ordered_names': ORDERED_GENERAL_INVENTORY_NAME,
            'additional_filters': None,
            'msg': "Inventory Breakdown"
        },
        'inventory_notes': {
            'id_filter': "1632000",
            'ordered_names': ORDERED_GENERAL_INVENTORY_NOTES_NAME,
            'additional_filters': None,
            'drop_cols': ['id', 'unitRef', 'precision'],
            'msg': "Inventory Notes"
        },
        'cogs_breakdown': {
            'id_filter': "1670000",
            'ordered_names': ORDERED_GENERAL_COGS_NAME,
            'additional_filters': None,
            'drop_cols': ['id', 'unitRef', 'precision'],
            'msg': "COGS Breakdown"
        },
        'cogs_notes': {
            'id_filter': "1671000",
            'ordered_names': ORDERED_GENERAL_COGS_NOTES_NAME,
            'additional_filters': None,
            'drop_cols': ['id', 'unitRef', 'precision'],
            'msg': "COGS Notes"
        },
        'revenue_by_parties': {
            'id_filter': ['1616000', '1617000'],
            'ordered_names': ORDERED_REV_BY_PARTIES_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Service') &
                    ~combined_df.context.str.contains('Product') &
                    ~combined_df.name.str.contains('Service') &
                    ~combined_df.name.str.contains('Product')
                ) |
                (df.name.isin(['SalesAndRevenue']) &
                 combined_df.context.isin(['CurrentYearDuration']))
            ),
            'preprocess': lambda df: df.assign(
                # processed_id='IXF1210000E02',
                name=df['name'] + "_" + df['context'].str.split("_").str[-1]
            ),
            'msg': "Revenue by Parties"
        },
        'revenue_by_type': {
            'id_filter': '1617000',
            'ordered_names': ORDERED_REV_BY_TYPE_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Party') &
                    ~combined_df.context.str.contains('Parties') &
                    ~combined_df.name.str.contains('Party') &
                    ~combined_df.name.str.contains('Parties')
                ) |
                (df.name.isin(['SalesAndRevenue']) &
                 combined_df.context.isin(['CurrentYearDuration']))
            ),
            'preprocess': lambda df: df.assign(
                # processed_id='IXF1210000E02',
                name=df['name'] + "_" + df['context'].str.split("_").str[-1]
            ),
            'msg': "Revenue by Type"
        },
        'revenue_by_source': {
            'id_filter': '1618000',
            'ordered_names': ORDERED_REV_BY_SOURCE_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Party') &
                    ~combined_df.context.str.contains('Service') &
                    ~combined_df.context.str.contains('Product') &
                    ~combined_df.context.str.contains('Parties') &
                    ~combined_df.name.str.contains('Party') &
                    ~combined_df.name.str.contains('Parties')
                )
            ),
            'preprocess': lambda df: df.assign(
                # processed_id='IXF1210000E02',
                name=df['name'] + "_" + df['context'].str.split("_").str[-1]
            ),
            'msg': "Revenue by Source"
        },
        'revenue_morethan_10percent': {
            'id_filter': '1619000',
            'ordered_names': ORDERED_REV_MORE_THAN_10_PERCENT_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Related') &
                    ~combined_df.context.str.contains('Third')
                )
            ),
            'preprocess': lambda df: df.assign(
                # processed_id='IXF1210000E02',
                name=(df['name'] + "_" + df['context'].str.split("_").str[-1]
                      ).str.replace('PriorYearDuration', 'CurrentYearDuration')
            ),
            'msg': "Revenue by Source"
        },
        'receivable_by_currency': {
            'id_filter': '1620100',
            'ordered_names': ORDERED_RECEIVABLE_CURRENCY_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Days') &
                    ~combined_df.context.str.contains('NotYet') &
                    ~combined_df.context.str.contains('Rank') &
                    ~combined_df.context.str.contains('Overdue')
                )
            ),
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_" + \
                df['context'].str.extract(
                    r'(?:PriorEndYearInstant_|CurrentYearInstant_\d+_)?((?:(?:[A-Z]{3}|OtherCurrency|OthersCounterparty)Member_)?(?:ThirdPartyMember|RelatedPartyMember))')[0].fillna('')
            ),
            'msg': "Receivable by Currency"
        },
        'receivable_by_aging': {
            'id_filter': ['1620200', '1620500', '1620400'],
            'ordered_names': ORDERED_RECEIVABLE_AGING_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('RelatedParty') &
                    ~combined_df.context.str.contains('ThirdParty') &
                    ~combined_df.context.str.contains('Domestic') &
                    ~combined_df.context.str.contains('International')
                )
            ),
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_" + \
                df['context'].str.extract(
                    r'_((?:[A-Za-z0-9]+(?:To[A-Za-z0-9]+)?(?:DaysMember|Instant))_(?:NotYetDueMember|OverdueMember)|(?:[A-Za-z0-9]+(?:To[A-Za-z0-9]+)?(?:DaysMember|Instant))|(?:NotYetDueMember|OverdueMember))')[0].fillna('')
            ),
            'msg': "Receivable by Aging"
        },
        'receivable_by_parties': {
            'id_filter': '1620300',
            'ordered_names': ORDERED_RECEIVABLE_PARTY_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Days') &
                    ~combined_df.context.str.contains('NotYet') &
                    ~combined_df.context.str.contains('IDR|AUD|CAD|CNY|EUR|HKD|GBP|JPY|SGD|THB|USD|Currency') &
                    ~combined_df.context.str.contains('Overdue')
                )
            ),
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_"
                + df['context'].str.split("_").str[-2].fillna('') + "_" \
                + df['context'].str.split("_").str[-1].fillna('')
            ),
            'msg': "Receivable by Parties"
        },
        'receivable_allowances': {
            'id_filter': '1620500',
            'ordered_names': ORDERED_RECEIVABLE_ALLOWANCE_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Days') &
                    ~combined_df.context.str.contains('NotYet') &
                    ~combined_df.context.str.contains('IDR|AUD|CAD|CNY|EUR|HKD|GBP|JPY|SGD|THB|USD|Currency') &
                    ~combined_df.context.str.contains('Overdue')
                )
            ),
            'msg': "Receivable by Allowances"
        },
        'receivable_by_area': {
            'id_filter': ['1620400', '1620500'],
            'ordered_names': ORDERED_RECEIVABLE_AREA_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Days') &
                    ~combined_df.context.str.contains('NotYet') &
                    ~combined_df.context.str.contains('IDR|AUD|CAD|CNY|EUR|HKD|GBP|JPY|SGD|THB|USD|Currency') &
                    ~combined_df.context.str.contains('Overdue') &
                    ~combined_df.context.str.contains('ThirdParty') &
                    ~combined_df.context.str.contains('RelatedParty')
                )
            ),
            'preprocess': lambda df: df.assign(
                name=(df['name'] + "_" + df['context'].str.split("_").str[-1]
                      ).str.replace('PriorEndYearInstant', 'CurrentYearInstant')
            ),
            'msg': "Receivable by Area"
        },
        'payable_by_currency': {
            'id_filter': '1640100',
            'ordered_names': ORDERED_PAYABLE_CURRENCY_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Rank') &
                    ~combined_df.context.str.contains('Counterparty')
                )
            ),
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_" +
                df['context'].str.extract(
                    r'(?:PriorEndYearInstant_|CurrentYearInstant_\d+_)?((?:(?:[A-Z]{3}|OtherCurrency|OthersCounterparty)Member_)?(?:ThirdPartyMember|RelatedPartyMember))')[0].fillna('')
            ),
            'msg': "Receivable by Currency"
        },
        'payable_by_aging': {
            'id_filter': '1640200',
            'ordered_names': ORDERED_PAYABLE_AGING_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('RelatedParty') &
                    ~combined_df.context.str.contains('ThirdParty') &
                    ~combined_df.context.str.contains('Domestic') &
                    ~combined_df.context.str.contains('International')
                )
            ),
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_" + \
                df['context'].str.extract(
                    r'_((?:[A-Za-z0-9]+(?:To[A-Za-z0-9]+)?(?:DaysMember|Instant))_(?:NotYetDueMember|OverdueMember)|(?:[A-Za-z0-9]+(?:To[A-Za-z0-9]+)?(?:DaysMember|Instant))|(?:NotYetDueMember|OverdueMember))')[0].fillna('')
            ),
            'msg': "Payable by Aging"
        },
        'payable_by_parties': {
            'id_filter': '1640300',
            'ordered_names': ORDERED_PAYABLE_PARTY_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains(
                        'IDR|AUD|CAD|CNY|EUR|HKD|GBP|JPY|SGD|THB|USD|Currency')
                )
            ),
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_"
                + df['context'].str.split("_").str[-2].fillna('') + "_" \
                + df['context'].str.split("_").str[-1].fillna('')
            ),
            'msg': "Payable by Parties"
        },
        'long_term_bank_loan_value': {
            'id_filter': '1691000a',
            'ordered_names': ORDERED_LT_BANK_LOAN_NAME,
            'additional_filters': None,
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_" +
                df['context'].str.extract(
                    r"_((?:[A-Za-z][A-Za-z0-9\s]*Member)_(?:[A-Z]{3}Member|OtherCurrencyMember)|(?:[A-Z]{3}Member|OtherCurrencyMember)|(?:[A-Za-z][A-Za-z0-9\s]*Member))")[0].fillna('')
            ),
            'msg': "Long Term Bank Loan Value"
        },
        'long_term_bank_loan_notes': {
            'id_filter': "1691100",
            'ordered_names': ORDERED_LT_BANK_LOAN_NOTES_NAME,
            'additional_filters': None,
            'drop_cols': ['id', 'unitRef', 'precision'],
            'msg': "Inventory Notes"
        },
        'long_term_bank_loan_interest': {
            'id_filter': '1692000',
            'ordered_names': ORDERED_LT_BANK_INTEREST_NAME,
            'additional_filters': None,
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_" + \
                df['context'].str.extract(
                    r"_((?:[A-Za-z][A-Za-z0-9\s]*Member)_(?:[A-Z]{3}Member|OtherCurrencyMember)|(?:[A-Z]{3}Member|OtherCurrencyMember)|(?:[A-Za-z][A-Za-z0-9\s]*Member))")[0].fillna('')
            ),
            'msg': "Long Term Bank Loan Interest"
        },
        'short_term_bank_loan_value': {
            'id_filter': '1693000',
            'ordered_names': ORDERED_ST_BANK_LOAN_NAME,
            'additional_filters': None,
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_" +
                df['context'].str.extract(
                    r"_((?:[A-Za-z][A-Za-z0-9\s]*Member)_(?:[A-Z]{3}Member|OtherCurrencyMember)|(?:[A-Z]{3}Member|OtherCurrencyMember)|(?:[A-Za-z][A-Za-z0-9\s]*Member))")[0].fillna('')
            ),
            'msg': "Short Term Bank Loan Value"
        },
        'short_term_bank_loan_notes': {
            'id_filter': "1693100",
            'ordered_names': ORDERED_ST_BANK_LOAN_NOTES_NAME,
            'additional_filters': None,
            'drop_cols': ['id', 'unitRef', 'precision'],
            'msg': "Short Term Bank Loan Notes"
        },
        'short_term_bank_loan_interest': {
            'id_filter': '1696000',
            'ordered_names': ORDERED_ST_BANK_INTEREST_NAME,
            'additional_filters': None,
            'preprocess': lambda df: df.assign(
                name=df['name'] + "_" +
                df['context'].str.extract(
                    r"_((?:[A-Za-z][A-Za-z0-9\s]*Member)_(?:[A-Z]{3}Member|OtherCurrencyMember)|(?:[A-Z]{3}Member|OtherCurrencyMember)|(?:[A-Za-z][A-Za-z0-9\s]*Member))")[0].fillna('')
            ),
            'msg': "Short Term Bank Loan Interest"
        }
    }

    cfg = config[table_type]
    print(f"Getting {cfg['msg']} table....")

    # Base filtering
    if isinstance(cfg['id_filter'], list):
        # print('Multiple Id to filter..')
        id_condition = combined_df.processed_id.str.contains(
            '|'.join(cfg['id_filter']), na=False)
    else:
        id_condition = combined_df.processed_id.str.contains(
            cfg['id_filter'], na=False)

    raw_df = combined_df[id_condition]

    # Apply additional filters
    if cfg['additional_filters']:
        if any(
            string in table_type for string in [
                'revenue',
                'receivable',
                'payable']):
            additional_mask = cfg['additional_filters'](raw_df)
            raw_df = pd.DataFrame(raw_df[additional_mask])
        else:
            additional_mask = cfg['additional_filters'](combined_df)
            raw_df = pd.concat([raw_df, combined_df[additional_mask]])

    # Preprocessing
    raw_df = raw_df.sort_values(['name', 'year']).reset_index(drop=True)

    if 'preprocess' in cfg:
        raw_df = cfg['preprocess'](raw_df)

    # Name ordering and deduplication
    df_unique_names = raw_df['name'].unique()
    ordered_set = set(cfg['ordered_names'])
    final_order = [n for n in cfg['ordered_names'] if n in df_unique_names]
    # print(combined_df.shape[0])
    # print(raw_df.shape[0])
    missing = [n for n in df_unique_names if n not in ordered_set]

    if missing:
        print(f"Missing elements in ordered list: {missing}. Removing Rows..")
        for x in missing:
            raw_df = raw_df[raw_df.name != x]
        # exit()

    raw_df['name'] = pd.Categorical(
        raw_df['name'],
        categories=final_order,
        ordered=True)
    df_sorted = raw_df.sort_values(['name', 'year']).reset_index(drop=True)
    df_sorted = df_sorted.drop_duplicates(subset=['name', 'year'], keep='first')

    # Universal normalization using row-wise function
    if table_type not in [
        'general_info',
        'accounting_policies',
        'inventory_notes',
        'cogs_notes',
        'long_term_bank_loan_notes',
        'long_term_bank_loan_interest',
        'short_term_bank_loan_notes',
            'short_term_bank_loan_interest']:  # Skip for non-financial tables
        df_sorted['value'] = df_sorted.apply(
            normalize_multiplier_value,
            convert_billion_idr=convert_billion_idr,
            convert_million_usd=convert_million_usd,
            axis=1
        )

    if 'drop_cols' in cfg:
        raw_df.drop(cfg['drop_cols'], axis=1, inplace=True, errors='ignore')

    # Create complete multi-index
    unique_names = df_sorted['name'].unique()
    unique_years = df_sorted['year'].unique()
    multi_idx = pd.MultiIndex.from_product(
        [unique_names, unique_years],
        names=['name', 'year']
    )

    # Handle missing combinations
    tidy_df = (
        df_sorted.set_index(['name', 'year'])
        .reindex(multi_idx)
        .reset_index()
    )
    tidy_df.drop(['context', 'decimals', 'processed_id'],
                 axis=1, inplace=True, errors='ignore')

    # Pivot and format names
    tidy_pivot = tidy_df.pivot(
        index='name',
        columns='year',
        values='value').reset_index()
    name_map = pd.read_csv(name_mapping_path)
    name_dict = dict(zip(name_map.xbrl_name, name_map.formatted_name))
    tidy_pivot['formatted_name'] = tidy_pivot['name'].map(name_dict)
    tidy_pivot.insert(1, 'formatted_name', tidy_pivot.pop('formatted_name'))

    return tidy_pivot


def get_finance_financial_table(
    combined_df: pd.DataFrame,
    name_mapping_path: str,
    table_type: str,
    convert_billion_idr: bool,
    convert_million_usd: bool
) -> pd.DataFrame:
    """Generate standardized financial tables with consistent normalization"""
    config = {
        'general_info': {
            'id_filter': "1000000",
            'ordered_names': ORDERED_GI_NAME,
            'additional_filters': None,
            'drop_cols': ['id', 'unitRef', 'precision'],
            'msg': "General Info"
        },
        'balance_sheet': {
            'id_filter': "4220000",
            'ordered_names': ORDERED_FINANCE_BS_NAME,
            'additional_filters': lambda df: (
                df.name.isin([
                    "PropertyPlantAndEquipment", "PropertyAndEquipment", 'TranslationAdjustment',
                    'AllowanceForImpairmentLossesForLoans', 'AllowanceForImpairmentLossesForMurabahahReceivables',
                    'AllowanceForImpairmentLossesForIstishnaReceivables', 'AllowanceForImpairmentLossesForIjarahReceivables',
                    'AllowanceForImpairmentLossesForQardhFunds', 'AllowanceForImpairmentLossesForMudharabahFinancing',
                    'AllowanceForImpairmentLossesForMusyarakahFinancing'
                ]) &
                df.context.isin(["PriorEndYearInstant", "CurrentYearInstant"])
            ),
            'preprocess': lambda df: df.assign(
                processed_id='IXF4220000E02',
                name=df['name'].str.replace('PropertyAndEquipment', 'PropertyPlantAndEquipment')
            ),
            'msg': "Balance Sheet"
        },
        'income_statement': {
            'id_filter': ["4312000", "4322000"],
            'ordered_names': ORDERED_FINANCE_IS_NAME,
            'additional_filters': None,
            'msg': "Income Statement"
        },
        'cash_flow': {
            'id_filter': "4510000",
            'ordered_names': ORDERED_FINANCE_CF_NAME,
            'additional_filters': None,
            'msg': "Cash Flow"
        },
        'accounting_policies': {
            'id_filter': "4610000",
            'ordered_names': ORDERED_FINANCE_AP_NAME,
            'additional_filters': None,
            'msg': "Accounting Policies"
        },
        'credit_by_currency': {
            'id_filter': ["4611100a", "4613100a", "4614100"],
            'ordered_names': ORDERED_FINANCE_CREDIT_CURRENCY_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Manufacturing|Trading|Agriculture|BusinessServices|'
                                                      'Construction|Transportation|Electricity|SocialServices|Mining|Property|OtherSectors') &
                    ~combined_df.context.str.contains('CurrentMember|SpecialMention|Substandard|Doubtful|Loss') &
                    ~combined_df.context.str.contains('WorkingCapitalMember|InvestmentMember|SyndicatedMember|GovernmentProgramsMember|'
                                                      'ExportMember|OtherSubtotalLoansMember|ConsumerMember|EmployeeMember')
                )
            ),
            'msg': "Credit by Currency",
            'preprocess': lambda df: df.assign(
                name=df['name'] +
                df['context'].str.findall(r'(ConventionalLoansMember|ShariaLoansMember|ThirdPartiesMember|RelatedPartiesMember|RupiahMember|ForeignCurrenciesMember)').str.join('_').apply(lambda x: f'_{x}' if x else '')
            ),
        },
        'credit_by_type': {
            'id_filter': "4612100a",
            'ordered_names': ORDERED_FINANCE_CREDIT_TYPE_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('Manufacturing|Trading|Agriculture|BusinessServices|'
                                                      'Construction|Transportation|Electricity|SocialServices|Mining|Property|OtherSectors')
                )
            ),
            'msg': "Credit by Type",
            'preprocess': lambda df: df.assign(
                name=df['name'] +
                df['context'].str.findall(r'(WorkingCapitalMember|InvestmentMember|SyndicatedMember|GovernmentProgramsMember|ExportMember|OthersSubtotalLoansMember|ConsumerMember|EmployeeMember|RupiahMember|ForeignCurrenciesMember|CurrentMember|SpecialMention|Substandard|Doubtful|Loss)').str.join('_').apply(lambda x: f'_{x}' if x else '')
            ),
        },
        'credit_by_sector': {
            'id_filter': "4613100a",
            'ordered_names': ORDERED_FINANCE_CREDIT_SECTOR_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('WorkingCapitalMember|InvestmentMember|SyndicatedMember|GovernmentProgramsMember|'
                                                      'ExportMember|OtherSubtotalLoansMember|ConsumerMember|EmployeeMember')
                )
            ),
            'msg': "Credit by Type",
            'preprocess': lambda df: df.assign(
                name=df['name'] +
                df['context'].str.findall(r'(ManufacturingMember|TradingRestaurantsHotelsMember|AgricultureMember|BusinessServicesMember|ConstructionMember|TransportationWarehousingCommunicationsMember|ElectricityGasWaterMember|SocialServicesMember|MiningMember|PropertyMember|OtherSectorsMember|RupiahMember|ForeignCurrenciesMember|CurrentMember|SpecialMention|Substandard|Doubtful|Loss)').str.join('_').apply(lambda x: f'_{x}' if x else '')
            ),
        },
        'credit_other': {
            'id_filter': "4614100",
            'ordered_names': ORDERED_FINANCE_CREDIT_OTHER_NAME,
            'additional_filters': lambda df: (
                (
                    ~combined_df.context.str.contains('CurrentMember|SpecialMention|Substandard|Doubtful|Loss') &
                    ~combined_df.context.str.contains('WorkingCapitalMember|InvestmentMember|SyndicatedMember|GovernmentProgramsMember|'
                                                      'ExportMember|OtherSubtotalLoansMember|ConsumerMember|EmployeeMember')
                )
            ),
            'msg': "Credit Others"
        },
        'savings_breakdown': {
            'id_filter': "4622100",
            'ordered_names': ORDERED_FINANCE_SAVINGS_NAME,
            'additional_filters': None,
            'msg': "Savings Breakdown",
            'preprocess': lambda df: df.assign(
                name=df['name'] +
                df['context'].str.findall(r'(ThirdPartiesMember|RelatedPartiesMember|RupiahMember|ForeignCurrenciesMember)').str.join('_').apply(lambda x: f'_{x}' if x else '')
            ),
        },
        'giro_breakdown': {
            'id_filter': "4621100",
            'ordered_names': ORDERED_FINANCE_GIRO_NAME,
            'additional_filters': None,
            'msg': "Giro Breakdown",
            'preprocess': lambda df: df.assign(
                name=df['name'] +
                df['context'].str.findall(r'(ThirdPartiesMember|RelatedPartiesMember|RupiahMember|ForeignCurrenciesMember)').str.join('_').apply(lambda x: f'_{x}' if x else '')
            ),
        },
        'deposito_breakdown': {
            'id_filter': "4623100",
            'ordered_names': ORDERED_FINANCE_DEPOSITO_NAME,
            'additional_filters': None,
            'msg': "Deposito Breakdown",
            'preprocess': lambda df: df.assign(
                name=df['name'] +
                df['context'].str.findall(r'(ThirdPartiesMember|RelatedPartiesMember|RupiahMember|ForeignCurrenciesMember)').str.join('_').apply(lambda x: f'_{x}' if x else '')
            ),
        },
        'deposit_interest': {
            'id_filter': "4624100",
            'ordered_names': ORDERED_FINANCE_DEPOSIT_INTEREST_NAME,
            'additional_filters': None,
            'msg': "Deposit Interest",
            'preprocess': lambda df: df.assign(
                name=df['name'] +
                df['context'].str.findall(r'(RupiahMember|ForeignCurrenciesMember)').str.join('_').apply(lambda x: f'_{x}' if x else '')
            ),
        },
        'interest_revenue': {
            'id_filter': "4631100",
            'ordered_names': ORDERED_FINANCE_INTEREST_REV_NAME,
            'additional_filters': None,
            'msg': "Interest Revenue breakdown"
        },
        'interest_expense': {
            'id_filter': "4632100",
            'ordered_names': ORDERED_FINANCE_INTEREST_EXPENSE_NAME,
            'additional_filters': None,
            'msg': "Interest Expense breakdown"
        },
    }

    cfg = config[table_type]
    print(f"Getting {cfg['msg']} table....")

    # Base filtering
    if isinstance(cfg['id_filter'], list):
        id_condition = combined_df.processed_id.str.contains(
            '|'.join(cfg['id_filter']), na=False)
    else:
        id_condition = combined_df.processed_id.str.contains(
            cfg['id_filter'], na=False)

    raw_df = combined_df[id_condition]

    # Apply additional filters
    if cfg['additional_filters']:
        if table_type == 'balance_sheet':
            additional_mask = cfg['additional_filters'](combined_df)
            raw_df = pd.concat([raw_df, combined_df[additional_mask]])
        else:
            additional_mask = cfg['additional_filters'](raw_df)
            raw_df = pd.DataFrame(raw_df[additional_mask])

    # Preprocessing
    raw_df = raw_df.sort_values(['name', 'year']).reset_index(drop=True)

    if 'preprocess' in cfg:
        raw_df = cfg['preprocess'](raw_df)

    # Name ordering and deduplication
    df_unique_names = raw_df['name'].unique()
    ordered_set = set(cfg['ordered_names'])
    final_order = [n for n in cfg['ordered_names'] if n in df_unique_names]
    # print(combined_df.shape[0])
    # print(raw_df.shape[0])
    missing = [n for n in df_unique_names if n not in ordered_set]

    if missing:
        print(f"Missing elements in ordered list: {missing}. Removing Rows..")
        for x in missing:
            raw_df = raw_df[raw_df.name != x]
        # exit()

    raw_df['name'] = pd.Categorical(
        raw_df['name'],
        categories=final_order,
        ordered=True)
    df_sorted = raw_df.sort_values(['name', 'year']).reset_index(drop=True)
    df_sorted = df_sorted.drop_duplicates(subset=['name', 'year'], keep='first')

    # Universal normalization using row-wise function
    if table_type != 'general_info':  # Skip for non-financial tables
        df_sorted['value'] = df_sorted.apply(
            normalize_multiplier_value,
            convert_billion_idr=convert_billion_idr,
            convert_million_usd=convert_million_usd,
            axis=1
        )

    # print("Creating Multi Index")
    # Create complete multi-index
    unique_names = df_sorted['name'].unique()
    unique_years = df_sorted['year'].unique()
    multi_idx = pd.MultiIndex.from_product(
        [unique_names, unique_years],
        names=['name', 'year']
    )

    # print("Handle Missing Combination")
    # Handle missing combinations
    tidy_df = (
        df_sorted.set_index(['name', 'year'])
        .reindex(multi_idx)
        .reset_index()
    )
    tidy_df.drop(['context', 'decimals', 'processed_id'],
                 axis=1, inplace=True, errors='ignore')

    # Pivot and format names
    # print("Pivot table")
    tidy_pivot = tidy_df.pivot(
        index='name',
        columns='year',
        values='value').reset_index()
    name_map = pd.read_csv(name_mapping_path)
    name_dict = dict(zip(name_map.xbrl_name, name_map.formatted_name))
    tidy_pivot['formatted_name'] = tidy_pivot['name'].map(name_dict)
    tidy_pivot.insert(1, 'formatted_name', tidy_pivot.pop('formatted_name'))
    # print(tidy_pivot)
    # print("Returning value")

    return tidy_pivot
