import pandas as pd
import time
import json
import requests
import datetime
import telegram
import configparser
import os
import sys

telegram_info                       = configparser.RawConfigParser()
telegram_info.read('config.ini')

try:
    telegram_bot_token              = telegram_info['telegram']['bottoken']
    telegram_chatid                 = telegram_info['telegram']['chatid']
except KeyError:
    os.system("cls" if os.name == "nt" else "clear")
    print("Run setup.py first")
    sys.exit(1)

# Enter BUID (Binance User ID) of targeted account
TARGETED_ACCOUNT_UID                = ""

ACCOUNT_INFO_URL                    = f'https://www.binance.com/en/futures-activity/leaderboard/user?encryptedUid={TARGETED_ACCOUNT_UID}'

headers                             = {
    'authority'                     : 'www.binance.com',
    'accept'                        : '*/*',
    'accept-language'               : 'en-US,en;q=0.9',
    'bnc-uuid'                      : '0202c537-8c2b-463a-bdef-33761d21986a',
    'clienttype'                    : 'web',
    'csrftoken'                     : 'd41d8cd98f00b204e9800998ecf8427e',
    'device-info'                   : 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA4MCIsImF2YWlsYWJsZV9zY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA0MCIsInN5c3RlbV92ZXJzaW9uIjoiV2luZG93cyAxMCIsImJyYW5kX21vZGVsIjoidW5rbm93biIsInN5c3RlbV9sYW5nIjoicnUtUlUiLCJ0aW1lem9uZSI6IkdNVCszIiwidGltZXpvbmVPZmZzZXQiOi0xODAsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTAxLjAuNDk1MS42NyBTYWZhcmkvNTM3LjM2IiwibGlzdF9wbHVnaW4iOiJQREYgVmlld2VyLENocm9tZSBQREYgVmlld2VyLENocm9taXVtIFBERiBWaWV3ZXIsTWljcm9zb2Z0IEVkZ2UgUERGIFZpZXdlcixXZWJLaXQgYnVpbHQtaW4gUERGIiwiY2FudmFzX2NvZGUiOiI1ZjhkZDMyNCIsIndlYmdsX3ZlbmRvciI6Ikdvb2dsZSBJbmMuIChJbnRlbCkiLCJ3ZWJnbF9yZW5kZXJlciI6IkFOR0xFIChJbnRlbCwgSW50ZWwoUikgVUhEIEdyYXBoaWNzIDYyMCBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKSIsImF1ZGlvIjoiMTI0LjA0MzQ3NTI3NTE2MDc0IiwicGxhdGZvcm0iOiJXaW4zMiIsIndlYl90aW1lem9uZSI6IkV1cm9wZS9Nb3Njb3ciLCJkZXZpY2VfbmFtZSI6IkNocm9tZSBWMTAxLjAuNDk1MS42NyAoV2luZG93cykiLCJmaW5nZXJwcmludCI6IjE5YWFhZGNmMDI5ZTY1MzU3N2Q5OGYwMmE0NDE4Nzc5IiwiZGV2aWNlX2lkIjoiIiwicmVsYXRlZF9kZXZpY2VfaWRzIjoiMTY1MjY4OTg2NTQwMGdQNDg1VEtmWnVCeUhONDNCc2oifQ==',
    'fvideo-id'                     : '3214483f88c0abbba34e5ecf5edbeeca1e56e405',
    'lang'                          : 'en',
    'origin'                        : 'https://www.binance.com',
    'referer'                       : ACCOUNT_INFO_URL,
    'sec-ch-ua'                     : '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile'              : '?0',
    'sec-ch-ua-platform'            : '"Windows"',
    'sec-fetch-dest'                : 'empty',
    'sec-fetch-mode'                : 'cors',
    'sec-fetch-site'                : 'same-origin',
    'user-agent'                    : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    'x-trace-id'                    : 'e9d5223c-5d71-4834-8563-c253a1fc3ae8',
    'x-ui-request-trace'            : 'e9d5223c-5d71-4834-8563-c253a1fc3ae8',
}

json_data                           = {
    'encryptedUid'                  : TARGETED_ACCOUNT_UID,
    'tradeType'                     : 'PERPETUAL',
}

bot                                 = telegram.Bot(token=telegram_bot_token)

def telegram_send_message(message):
    apiURL                          = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    try:
        response                    = requests.post(apiURL, json={'chat_id': telegram_chatid, 'text': message, 'parse_mode': 'html', 'disable_web_page_preview': True})
        print(response.text)
    except Exception as e:
        print(e)

# odifying DataFrame, including calculating estimated entry size in USDT
def modify_data(data) -> pd.DataFrame:
    df                              = pd.DataFrame(data)
    position                        = pd.DataFrame(df['data'][0]).set_index('symbol')
    position['estimatedEntrySize']  = round((abs(position['amount']) / position['leverage']) * position['entryPrice'], 2)
    position['pnl']                 = round(position['pnl'], 2)
    position.loc[(position['amount'] > 0), 'estimatedPosition'] = 'LONG'
    position.loc[(position['amount'] < 0), 'estimatedPosition'] = 'SHORT'
    position['updateTime']          = position['updateTime'].apply(lambda x: datetime.datetime(*x[:-1], x[-1] // 1000))
    position['updateTime']          = position['updateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    position_result                 = position[['estimatedPosition', 'leverage', 'estimatedEntrySize', 'amount',
                                                'entryPrice', 'markPrice', 'pnl', 'updateTime']]
    return position_result

# Getting position data from Binance API
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

# Getting market price from Binance API
def get_markprice(symbol):
    api_url                         = "https://fapi.binance.com/fapi/v1/premiumIndex"
    req_data                        = requests.get(api_url, params={"symbol": symbol})
    try:
        data                        = req_data.json()
        return data['markPrice']
    except Exception:
        return "Market price retrieval error"

previous_symbols                    = pd.Index([])
previous_position_result            = pd.DataFrame()
is_first_run                        = True

def send_new_position_message(symbol, row):
    estimated_position              = row['estimatedPosition']
    leverage                        = row['leverage']
    estimated_entry_size            = row['estimatedEntrySize']
    entry_price                     = row['entryPrice']
    pnl                             = row['pnl']
    updatetime                      = row['updateTime']
    message                         = f"<b>New position opened</b>\n\n" \
                                      f"Position: <b>{symbol} {estimated_position} {leverage}X</b>\n\n" \
                                      f"Base currency - USDT\n" \
                                      f"------------------------------\n" \
                                      f"Entry Price: {entry_price}\n" \
                                      f"Est. Entry Size: {estimated_entry_size}\n" \
                                      f"PnL: {pnl}\n\n" \
                                      f"Last Update:\n{updatetime} (UTC+0)\n" \
                                      f"<a href='{ACCOUNT_INFO_URL}'><b>VIEW PROFILE ON BINANCE</b></a>"
    telegram_send_message(message)

def send_closed_position_message(symbol, row):
    estimated_position              = row['estimatedPosition']
    leverage                        = row['leverage']
    updatetime                      = row['updateTime']
    message                         = f"<b>Position closed</b>\n\n" \
                                      f"Position: <b>{symbol} {estimated_position} {leverage}X</b>\n" \
                                      f"Current Price: {get_markprice(symbol)} USDT\n\n" \
                                      f"Last Update:\n{updatetime} (UTC+0)\n" \
                                      f"<a href='{ACCOUNT_INFO_URL}'><b>VIEW PROFILE ON BINANCE</b></a>"
    telegram_send_message(message)

def send_current_positions(position_result):
    if position_result.empty:
        telegram_send_message("<b>No positions found</b>")
    else:
        telegram_send_message("<b>Current positions:</b>")
        for symbol, row in position_result.iterrows():
            estimated_position      = row['estimatedPosition']
            leverage                = row['leverage']
            estimated_entry_size    = row['estimatedEntrySize']
            entry_price             = row['entryPrice']
            pnl                     = row['pnl']
            updatetime              = row['updateTime']
            message                 = f"Position: <b>{symbol} {estimated_position} {leverage}X</b>\n\n" \
                                      f"Base currency - USDT\n" \
                                      f"------------------------------\n" \
                                      f"Entry Price: {entry_price}\n" \
                                      f"Est. Entry Size: {estimated_entry_size}\n" \
                                      f"PnL: {pnl}\n\n" \
                                      f"Last Update:\n{updatetime} (UTC+0)\n" \
                                      f"<a href='{ACCOUNT_INFO_URL}'><b>VIEW PROFILE ON BINANCE</b></a>"
            telegram_send_message(message)

# Compare current data with previous data and send a message if there are any changes
# For first-time execution, send the entire position that the target currently holds.
while True:
    response                        = get_position(headers, json_data)
    if response is not None:
        leaderboard_data            = json.loads(response.text)
        position_result             = modify_data(leaderboard_data)

        new_symbols                 = position_result.index.difference(previous_symbols)
        if not is_first_run and not new_symbols.empty:
            for symbol in new_symbols:
                send_new_position_message(symbol, position_result.loc[symbol])

        closed_symbols              = previous_symbols.difference(position_result.index)
        if not is_first_run and not closed_symbols.empty:
            for symbol in closed_symbols:
                if symbol in previous_position_result.index:
                    send_closed_position_message(symbol, previous_position_result.loc[symbol])

        if is_first_run:
            send_current_positions(position_result)

        previous_position_result    = position_result.copy()
        previous_symbols            = position_result.index.copy()
        is_first_run                = False
        time.sleep(300)