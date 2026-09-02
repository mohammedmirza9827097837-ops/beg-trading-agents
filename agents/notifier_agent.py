import os
import requests
from dotenv import load_dotenv

load_dotenv()

def notify(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, data={"chat_id": chat_id, "text": message})
    return response.json()

def notify_with_photo(message, photo_path):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(photo_path, "rb") as photo:
        response = requests.post(
            url,
            data={"chat_id": chat_id, "caption": message},
            files={"photo": photo}
        )
    return response.json()

if __name__ == "__main__":
    result = notify("BEG Trading Agents test message — sab sahi kaam kar raha hai!")
    print(result)
