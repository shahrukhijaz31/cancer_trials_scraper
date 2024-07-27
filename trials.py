"""This program scrap data from trials.scri.com and put the data into a csv"""

import json
import csv
import os
import urllib.parse
import requests

from dotenv import load_dotenv

payload = {}
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://trials.scri.com/search/1/Breast/1/74',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "\
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

load_dotenv()
token = os.getenv("PROXY_API_KEY")

cancers = [
    "Acute Lymphoblastic Leukemia",
    "Acute Myeloid Leukemia",
    "Amyloidosis", 
    "Breast",
    "Central Nervous System",
    "Chronic Lymphocytic Leukemia",
    "Chronic Myeloid Leukemia",
    "Gastrointestinal",
    "Genitourinary",
    "Graft vs Host",
    "Gynecologic",
    "Head and Neck",
    "Hematologic Refractory",
    "Hematopoietic Cell Transplantation",
    "Lung",
    "Lymphoma",
    "Molecular Profiling",
    "Multiple Disease Cohorts",
    "Multiple Myeloma",
    "Myelodysplastic Syndrome",
    "Myeloproliferative Neoplasms",
    "Other Cancers",
    "Pediatrics",
    "Refractory Malignancies",
    "Sarcoma",
    "Skin Cancers",
    "Thyroid Cancer",
    "Tissue"
]

csv_headers = ["officeName", "addressLine1", "addressLine2",
               "city", "state", "zipCode", "Cancer Type"]

with open("trials.csv", mode='w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)


    for cancer in cancers:
        CURRENT_PAGE = 1
        TOTAL_PAGE = 2

        while (CURRENT_PAGE < TOTAL_PAGE + 1):
            print(f"Scraping Page # {CURRENT_PAGE} for Cancer Type: {cancer}")

            url = f"https://trials.scri.com/api/v1/trials/search/1/{cancer}/{CURRENT_PAGE}"
            url = urllib.parse.quote(url)
            url = f"http://api.scrape.do?token={token}&url={url}"

            response = requests.request("GET", url, headers=headers, data=payload, timeout=20)
            response = json.loads(response.text)
            response = response["data"]

            TOTAL_PAGE = response["totalPageCount"]

            print(f"Total Pages are: {TOTAL_PAGE}")

            for result_data in response["searchResultsData"]:
                for office in result_data["offices"]:
                    office_data = [office["officeName"], office["addressLine1"],
                                office["addressLine2"], office["city"], office["state"],
                                office["zipCode"],
                                cancer, result_data["studyName"]]
                    writer.writerow(office_data)

            CURRENT_PAGE += 1

    file.close()
