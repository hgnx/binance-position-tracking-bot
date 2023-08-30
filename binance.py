import requests
import time
from message import telegram_send_message

def get_position(headers, json_data, max_retries=5):
    retry_count                     = 0
    while retry_count <= max_retries:
        try:
            return requests.post("https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition",
                                 headers=headers, json=json_data)
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
            telegram_send_message(f"Connection error occurred: {e}")
            if retry_count >= max_retries:
                telegram_send_message("Max retry count reached. Waiting for 10 minutes before next try...")
                time.sleep(600)
                retry_count         = 0
            else:
                print("Retrying in 5 seconds...")
                time.sleep(5)
                retry_count        += 1

def get_nickname(headers, json_data, max_retries=5):
    retry_count                     = 0
    while retry_count <= max_retries:
        try:
            return requests.post("https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo",
                                 headers=headers, json=json_data)
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {e}")
            telegram_send_message(f"Connection error occurred: {e}")
            if retry_count >= max_retries:
                telegram_send_message("Max retry count reached. Waiting for 10 minutes before next try...")
                time.sleep(600)
                retry_count         = 0
            else:
                print("Retrying in 5 seconds...")
                time.sleep(5)
                retry_count        += 1

def get_markprice(symbol):
    api_url                         = "https://fapi.binance.com/fapi/v1/premiumIndex"
    req_data                        = requests.get(api_url, params={"symbol": symbol})
    try:
        data                        = req_data.json()
        return data['markPrice']
    except Exception:
        return "Market price retrieval error"