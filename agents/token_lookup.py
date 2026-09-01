import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIP_FILE = os.path.join(BASE_DIR, "scrip_master.json")
SCRIP_MASTER_URL = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"

def download_scrip_master():
    print("Downloading scrip master (thoda time lagega, ~10MB file)...")
    response = requests.get(SCRIP_MASTER_URL)
    data = response.json()
    with open(SCRIP_FILE, "w") as f:
        json.dump(data, f)
    print(f"Saved {len(data)} instruments to {SCRIP_FILE}")
    return data

def find_token(symbol_name, exchange="NSE"):
    with open(SCRIP_FILE, "r") as f:
        data = json.load(f)
    results = []
    for item in data:
        if item.get("exch_seg") == exchange and symbol_name.upper() in item.get("symbol", "").upper():
            results.append(item)
    return results

if __name__ == "__main__":
    download_scrip_master()
