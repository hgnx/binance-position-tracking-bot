# Binance Futures Position Tracking Bot

The Binance Futures Position Tracking Bot is a Python script that utilizes the Binance API to monitor and record the trading activities of a specific trader on Binance Futures in real-time.

When the targeted trader opens a new position or closes an existing one, the script automatically detects these changes and sends an update notification via Telegram. This functionality enables users to follow the real-time trading activities of the targeted trader with detailed information about the latest positions including the estimated position, leverage, estimated entry size (in USDT), entry price, and profit and loss (PnL).

## Features

- Real-time monitoring and recording of a specific trader's trading positions on Binance Futures through the Binance API.
- Notifications via Telegram when a new position is opened or an existing one is closed.
- Detailed updates on each position, including estimated position, leverage, estimated entry size (in USDT), entry price (in USDT), profit and loss (PnL, in USDT), and update time.
- Efficient handling and analysis of tracked data using pandas DataFrame.
- Binance's API does not provide the value of positions in USDT. However, this script is designed to calculate the actual amount of USDT invested in a position, without considering leverage.
- Customizable setup for the Telegram bot token and chat ID, facilitated by the `setup.py` script.
- Continuous tracking and messaging system with 5-minute intervals for real-time data updates.
- Ability to track multiple accounts simultaneously. Each message includes the username, allowing for easy identification of individual user's trading positions.
- Error handling with retry mechanisms for potential connection failures.

## Setup

- Before running the main script (`main.py`), configure your Telegram bot token and chat ID using the `setup.py` script. You will be prompted to provide your Telegram bot token and chat ID, which will be stored in a config.ini file for the main script to reference.

## Installation and Usage

1. Download the project code.
```
git clone https://github.com/hgnx/binance-position-tracking-bot.git
```

2. Install the required libraries.
```
pip install -r requirements.txt
```

3. Contact [@Botfather](https://t.me/botfather) on Telegram to create a new bot and acquire the bot token.

4. Get the unique identifier for your group.
    - 4-1. Log in to [Telegram Web](https://web.telegram.org/a/) and navigate to the group where you want to receive notifications.
    - 4-2. Add the bot to the group.
    - 4-3. In the address bar, you'll find the URL that looks like this: "https://web.telegram.org/a/#-XXXXXXXXX". The sequence "**-XXXXXXXXX**" is your group's unique identifier.
    - 4-4. If your group is classified as a supergroup, prefix the unique identifier with "-100". For example, "**-100XXXXXXXXX**".

5. Run the setup script and enter your Telegram bot token and chat ID (the unique identifier of your group).
```
python setup.py
```

6. In `main.py`, assign the Binance UID (BUID) you want to track to the `TARGETED_ACCOUNT_UID` variable.
    - 6-1. This BUID can be found on the detailed page of the Binance Futures Leaderboard.
    - 6-2. Visit the [Binance Futures Leaderboard](https://www.binance.com/en/futures-activity/leaderboard/futures) and click on the user you want to track.
    - 6-3. In the address bar, you'll find the URL that looks like this: "https://www.binance.com/en/futures-activity/leaderboard/user/um?encryptedUid=XXXXXXXXX". The sequence "**XXXXXXXXX**" is the BUID.
    - 6-4. You can add as many BUIDs as you want to the list. However, adding too many BUIDs may cause connection issues.

7. Run the main script.
```
python main.py
```

## Example

### Current positions
  
![alt text](https://github.com/hgnx/binance-position-tracking-bot/blob/main/screenshots/current.png?raw=true)

### New position

![alt text](https://github.com/hgnx/binance-position-tracking-bot/blob/main/screenshots/new.png?raw=true)

### Closed position

![alt text](https://github.com/hgnx/binance-position-tracking-bot/blob/main/screenshots/closed.png?raw=true)

### Updated version

![alt text](https://github.com/hgnx/binance-position-tracking-bot/blob/main/screenshots/with_username.png?raw=true)

## Future Improvements
~~Currently, the script only tracks the positions of a single trader's account. It is technically feasible to track multiple accounts, however, identifying user nicknames based on the BUID (Binance UID) presents a challenge. On the Binance User profile page, the nickname initially displays as "--", and it updates to the actual nickname once the page fully loads.~~

~~One simple solution could be to use Selenium to fetch the nicknames, but incorporating this library for this single task might be excessive and not desirable for the implementation. The ability to fetch and associate nicknames is important for clarity when sending individual position tracking updates via Telegram. Thus, resolving the nickname identification issue could be an improvement for future update, as it would enable a clearer display of position tracking for individual users.~~

Now you can track multiple accounts simultaneously, and each username is also included in the message.

## Disclaimer
This script is for informational purposes only and should not be used as the basis for any financial decisions. I take no responsibility for any personal financial loss. Use this script at your own risk.