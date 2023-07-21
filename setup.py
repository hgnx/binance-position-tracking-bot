import os
import sys
import configparser

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Setup Wizard")

banner()

config_file                     = 'config.ini'

telegram_info                   = configparser.RawConfigParser()
telegram_info.add_section('telegram')

xbot                            = input("[+] Enter Telegram Bot Token: ")
telegram_info.set('telegram', 'bottoken', xbot)

xchat                           = input("[+] Enter Telegram ChatID : ")
telegram_info.set('telegram', 'chatid', xchat)

with open(config_file, 'w') as setup:
    telegram_info.write(setup)

print("[+] Setup completed successfully")