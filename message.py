import requests
import os
import sys
import configparser

telegram_info                       = configparser.RawConfigParser()
telegram_info.read('config.ini')

try:
    telegram_bot_token              = telegram_info['telegram']['bottoken']
    telegram_chatid                 = telegram_info['telegram']['chatid']
except KeyError:
    os.system("cls" if os.name == "nt" else "clear")
    print("Run setup.py first")
    sys.exit(1)

def telegram_send_message(message):
    apiURL                          = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage'
    try:
        response                    = requests.post(apiURL, json={'chat_id': telegram_chatid, 'text': message, 'parse_mode': 'html', 'disable_web_page_preview': True})
        print(response.text)
    except Exception as e:
        print(e)