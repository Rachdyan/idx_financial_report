import random
import urllib
import os
from zipfile import ZipFile
import requests

BASE_URL = "https://www.idx.co.id"
PERIOD_LIST = ["tw1", "tw2", "tw3", "audit"]

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
              " (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

USER_AGENT_ALT_1 = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) "
    "Gecko/20100101 Firefox/129.0"
)
USER_AGENT_ALT_2 = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0")

USER_AGENT_LIST = [USER_AGENT, USER_AGENT_ALT_1, USER_AGENT_ALT_2]

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

_FILE_PERIOD_MAP = {
    "Q1": "tw1",
    "Q2": "tw2",
    "Q3": "tw3",
    "FY": "audit"
}

PROXIES = None


# Use randomizer for user-agent to create various header's user agent for
# each call
def create_headers():
    used_user_agent = random.choice(USER_AGENT_LIST)
    used_headers = HEADERS
    used_headers["User-Agent"] = used_user_agent
    # print(used_headers)
    return used_headers


def generate_filename(symbol: str, year: int, period: str):
    symbol = symbol.replace(".JK", "")
    # file_period = _FILE_PERIOD_MAP[period]
    return f"./data/{symbol}/{symbol}-{year}-{period}"


def generate_url(symbol: str, year: int, period: str):
    symbol = symbol.replace(".JK", "")
    file_period = _FILE_PERIOD_MAP[period]
    formatted_period = file_period.lower().upper()
    # file_period = _FILE_PERIOD_MAP[period]
    link = (f"https://www.idx.co.id/Portals/0/StaticData/ListedCompanies/"
            f"Corporate_Actions/New_Info_JSX/Jenis_Informasi/"
            f"01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan"
            f"//Laporan%20Keuangan%20Tahun%20{year}/{formatted_period}"
            f"/{symbol}/instance.zip")
    return link


# Call the API to download the Excel file data
def download_zip_file(url: str, filename: str, use_proxy: bool = False):
    try:
        print(f"[DOWNLOAD] Downloading from {url}")
        zip_filename = f"{filename}.zip"

        if not use_proxy:
            # Construct the request
            req = urllib.request.Request(url, headers=create_headers())

            # Open the request and write the response to a file
            response = urllib.request.urlopen(req)
            out_file = open(zip_filename, "wb")

            if int(response.getcode()) == 200:
                data = response.read()  # Read the response data
                out_file.write(data)  # Write the data to a file

                print("[EXTRACTING] Extracting instance.xbrl..")
                with ZipFile(zip_filename) as zObject:
                    zObject.extract(
                        "instance.xbrl",
                        path=f"{filename}"
                    )

                print("[DELETING] Deleting ZIP file..")
                os.remove(zip_filename)

            else:
                print(
                    f"[FAILED] Failed to get data status code "
                    f"{response.getcode()}")

        else:
            response = requests.get(
                url, allow_redirects=True, proxies=PROXIES, verify=False
            )

            if int(response.status_code) == 200:
                # Write the response content to a file
                with open(filename, "wb") as out_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        out_file.write(chunk)
            else:
                print(
                    f"[FAILED] Failed to get data status code "
                    f"{response.status_code}")

        return True
    except urllib.request.HTTPError as httper:
        print(
            f"[FAILED] Failed to download excel file for {filename}: {httper}")
        return False
    except Exception as e:
        print(f"[FAILED] Failed to download excel file for {filename}: {e}")
        return False
