<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<img src="readmeai/assets/logos/purple.svg" width="30%" style="position: relative; top: 0; right: 0;" alt="Project Logo"/>

# IDX_FINANCIAL_REPORT

<em></em>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/Rachdyan/idx_financial_report?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
<img src="https://img.shields.io/github/last-commit/Rachdyan/idx_financial_report?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/Rachdyan/idx_financial_report?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/Rachdyan/idx_financial_report?style=default&color=0080ff" alt="repo-language-count">

<!-- default option, no dependency badges. -->


<!-- default option, no dependency badges. -->

</div>
<br>

---

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
    - [Project Index](#project-index)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview



---

## Features

<code>❯ REPLACE-ME</code>

---

## Project Structure

```sh
└── idx_financial_report/
    ├── data
    │   └── .gitignore
    ├── get_financial_report.ipynb
    ├── result
    │   ├── .DS_Store
    │   ├── .gitignore
    │   ├── ANTM_Financial_Statement.xlsx
    │   ├── ARCI_Financial_Statement.xlsx
    │   ├── ARNA_Financial_Statement.xlsx
    │   ├── ARTO_Financial_Statement_Quarterly.xlsx
    │   ├── ASII_Financial_Statement.xlsx
    │   ├── ASII_Financial_Statement_Quarterly.xlsx
    │   ├── AUTO_Financial_Statement_Quarterly.xlsx
    │   ├── BBCA_Financial_Statement.xlsx
    │   ├── BBCA_Financial_Statement_Quarterly.xlsx
    │   ├── BBNI_Financial_Statement.xlsx
    │   ├── BBNI_Financial_Statement_Quarterly.xlsx
    │   ├── BBRI_Financial_Statement.xlsx
    │   ├── BBYB_Financial_Statement_Quarterly.xlsx
    │   ├── BMRI_Financial_Statement.xlsx
    │   ├── BNGA_Financial_Statement.xlsx
    │   ├── BRMS_Financial_Statement_Quarterly.xlsx
    │   ├── BUMI_Financial_Statement.xlsx
    │   ├── DEWA_Financial_Statement.xlsx
    │   ├── DRMA_Financial_Statement_Quarterly.xlsx
    │   ├── GEMS_Financial_Statement.xlsx
    │   ├── HAIS_Financial_Statement.xlsx
    │   ├── HRUM_Financial_Statement.xlsx
    │   ├── INDY_Financial_Statement.xlsx
    │   ├── KMTR_Financial_Statement_Quarterly.xlsx
    │   ├── NCKL_Financial_Statement.xlsx
    │   ├── NICL_Financial_Statement.xlsx
    │   ├── NISP_Financial_Statement.xlsx
    │   ├── NISP_Financial_Statement_Quarterly.xlsx
    │   ├── NOBU_Financial_Statement.xlsx
    │   ├── NOBU_Financial_Statement_Quarterly.xlsx
    │   ├── PSAB_Financial_Statement.xlsx
    │   ├── PTBA_Financial_Statement.xlsx
    │   ├── SMSM_Financial_Statement.xlsx
    │   ├── SUNI_Financial_Statement.xlsx
    │   ├── TBLA_Financial_Statement.xlsx
    │   ├── TBLA_Financial_Statement_Quarterly.xlsx
    │   ├── ~$ANTM_Financial_Statement.xlsx
    │   ├── ~$BBNI_Financial_Statement_Quarterly.xlsx
    │   ├── ~$BBYB_Financial_Statement_Quarterly.xlsx
    │   ├── ~$BRMS_Financial_Statement_Quarterly.xlsx
    │   ├── ~$KMTR_Financial_Statement_Quarterly.xlsx
    │   └── ~$TBLA_Financial_Statement_Quarterly.xlsx
    ├── schema
    │   ├── .DS_Store
    │   ├── all_general_information_1000000.csv
    │   ├── finance_accounting_policy_4610000.csv
    │   ├── finance_balance_sheet_4220000.csv
    │   ├── finance_cash_flow_4510000.csv
    │   ├── finance_credit_currency_4611100a.csv
    │   ├── finance_credit_other_4614100.csv
    │   ├── finance_credit_sector_4613100a.csv
    │   ├── finance_credit_type_4612100a.csv
    │   ├── finance_deposit_interest_4624100.csv
    │   ├── finance_deposito_4623100.csv
    │   ├── finance_giro_4621100.csv
    │   ├── finance_income_statement_4312000.csv
    │   ├── finance_interest_expense_4632100.csv
    │   ├── finance_interest_revenue_4631100.csv
    │   ├── finance_savings_4622100.csv
    │   ├── general_accounting_policy_1610000.csv
    │   ├── general_balance_sheet_1210000.csv
    │   ├── general_cash_flow_1510000.csv
    │   ├── general_cogs_1670000.csv
    │   ├── general_cogs_notes_1671000.csv
    │   ├── general_income_statement_1321000.csv
    │   ├── general_inventory_1630000.csv
    │   ├── general_inventory_notes_1632000.csv
    │   ├── general_lt_bank_interest_1692000.csv
    │   ├── general_lt_bank_loan_notes_1691100.csv
    │   ├── general_lt_bank_loans_value_169100a.csv
    │   ├── general_payable_by_aging_1640200.csv
    │   ├── general_payable_by_currency_1640100.csv
    │   ├── general_payable_by_parties_1640300.csv
    │   ├── general_receivable_allowances_1620500.csv
    │   ├── general_receivable_by_aging_1620200.csv
    │   ├── general_receivable_by_area_1620400.csv
    │   ├── general_receivable_by_currency_1620100.csv
    │   ├── general_receivable_by_parties_1620300.csv
    │   ├── general_revenue_10percent_1619000.csv
    │   ├── general_revenue_by_parties_1616000.csv
    │   ├── general_revenue_by_sources_1618000.csv
    │   ├── general_revenue_by_type_1617000.csv
    │   ├── general_st_bank_interest_1696000.csv
    │   ├── general_st_bank_loan_notes_1693100.csv
    │   └── general_st_bank_loans_value_1693000.csv
    ├── template
    │   ├── .DS_Store
    │   ├── .gitignore
    │   ├── Financial_Company_Template.xlsx
    │   └── General_Company_Template.xlsx
    └── utils
        ├── __init__.py
        ├── __pycache__
        ├── download_handler.py
        ├── excel_handler.py
        ├── ordered_name.py
        └── xbrl_handler.py
```

### Project Index

<details open>
	<summary><b><code>IDX_FINANCIAL_REPORT/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/get_financial_report.ipynb'>get_financial_report.ipynb</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- utils Submodule -->
	<details>
		<summary><b>utils</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ utils</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/utils/excel_handler.py'>excel_handler.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/utils/ordered_name.py'>ordered_name.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/utils/download_handler.py'>download_handler.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Rachdyan/idx_financial_report/blob/master/utils/xbrl_handler.py'>xbrl_handler.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
			</table>
		</blockquote>
	</details>
</details>

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python

### Installation

Build idx_financial_report from the source and intsall dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/Rachdyan/idx_financial_report
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd idx_financial_report
    ```

3. **Install the dependencies:**

echo 'INSERT-INSTALL-COMMAND-HERE'

### Usage

Run the project with:

echo 'INSERT-RUN-COMMAND-HERE'

### Testing

Idx_financial_report uses the {__test_framework__} test framework. Run the test suite with:

echo 'INSERT-TEST-COMMAND-HERE'

---

## Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

## Contributing

- **💬 [Join the Discussions](https://github.com/Rachdyan/idx_financial_report/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/Rachdyan/idx_financial_report/issues)**: Submit bugs found or log feature requests for the `idx_financial_report` project.
- **💡 [Submit Pull Requests](https://github.com/Rachdyan/idx_financial_report/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/Rachdyan/idx_financial_report
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/Rachdyan/idx_financial_report/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Rachdyan/idx_financial_report">
   </a>
</p>
</details>

---

## License

Idx_financial_report is protected under the [LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## Acknowledgments

- Credit `contributors`, `inspiration`, `references`, etc.

<div align="right">

[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
