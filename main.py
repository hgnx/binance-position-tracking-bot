import pandas as pd
import time
import json
import requests
import datetime
from misc import get_header, get_json
from message import telegram_send_message
from binance import get_position, get_nickname, get_markprice

# Enter BUID (Binance User ID) of targeted accounts
TARGETED_ACCOUNT_UIDs                = [
                                        "UID 1",
                                        "UID 2",
                                        "UID 3"
                                        ]

ACCOUNT_INFO_URL_TEMPLATE           = 'https://www.binance.com/en/futures-activity/leaderboard/user?encryptedUid={}'

# modifying DataFrame, including calculating estimated entry size in USDT
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

previous_symbols                    = {}
previous_position_results           = {}
is_first_runs                       = {uid: True for uid in TARGETED_ACCOUNT_UIDs}

def send_new_position_message(symbol, row, nickname):
    estimated_position              = row['estimatedPosition']
    leverage                        = row['leverage']
    estimated_entry_size            = row['estimatedEntrySize']
    entry_price                     = row['entryPrice']
    pnl                             = row['pnl']
    updatetime                      = row['updateTime']
    message                         = f"[<b>{nickname}</b>]\n<b>New position opened</b>\n\n" \
                                      f"Position: <b>{symbol} {estimated_position} {leverage}X</b>\n\n" \
                                      f"Base currency - USDT\n" \
                                      f"------------------------------\n" \
                                      f"Entry Price: {entry_price}\n" \
                                      f"Est. Entry Size: {estimated_entry_size}\n" \
                                      f"PnL: {pnl}\n\n" \
                                      f"Last Update:\n{updatetime} (UTC+0)\n" \
                                      f"<a href='{ACCOUNT_INFO_URL}'><b>VIEW PROFILE ON BINANCE</b></a>"
    telegram_send_message(message)

def send_closed_position_message(symbol, row, nickname):
    estimated_position              = row['estimatedPosition']
    leverage                        = row['leverage']
    updatetime                      = row['updateTime']
    message                         = f"[<b>{nickname}</b>]\n<b>Position closed</b>\n\n" \
                                      f"Position: <b>{symbol} {estimated_position} {leverage}X</b>\n" \
                                      f"Current Price: {get_markprice(symbol)} USDT\n\n" \
                                      f"Last Update:\n{updatetime} (UTC+0)\n" \
                                      f"<a href='{ACCOUNT_INFO_URL}'><b>VIEW PROFILE ON BINANCE</b></a>"
    telegram_send_message(message)

def send_current_positions(position_result, nickname):
    if position_result.empty:
        telegram_send_message(f"[<b>{nickname}</b>]\n<b>No positions found</b>")
    else:
        telegram_send_message(f"[<b>{nickname}</b>]\n<b>Current positions:</b>")
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

while True:
    try:
        for TARGETED_ACCOUNT_UID in TARGETED_ACCOUNT_UIDs:
            ACCOUNT_INFO_URL        = ACCOUNT_INFO_URL_TEMPLATE.format(TARGETED_ACCOUNT_UID)
            headers                 = get_header(ACCOUNT_INFO_URL)
            json_data               = get_json(TARGETED_ACCOUNT_UID)

            response_nickname       = get_nickname(headers, json_data)
            response                = get_position(headers, json_data)
            if response is not None and response_nickname is not None:
                nickname            = json.loads(response_nickname.text)['data']['nickName']
                leaderboard_data    = json.loads(response.text)
                position_result     = modify_data(leaderboard_data)

                new_symbols         = position_result.index.difference(previous_symbols.get(TARGETED_ACCOUNT_UID, pd.Index([])))
                if not is_first_runs[TARGETED_ACCOUNT_UID] and not new_symbols.empty:
                    for symbol in new_symbols:
                        send_new_position_message(symbol, position_result.loc[symbol], nickname)

                closed_symbols      = previous_symbols.get(TARGETED_ACCOUNT_UID, pd.Index([])).difference(position_result.index)
                if not is_first_runs[TARGETED_ACCOUNT_UID] and not closed_symbols.empty:
                    for symbol in closed_symbols:
                        if symbol in previous_position_results.get(TARGETED_ACCOUNT_UID, pd.DataFrame()).index:
                            send_closed_position_message(symbol, previous_position_results[TARGETED_ACCOUNT_UID].loc[symbol], nickname)

                if is_first_runs[TARGETED_ACCOUNT_UID]:
                    send_current_positions(position_result, nickname)

                previous_position_results[TARGETED_ACCOUNT_UID] = position_result.copy()
                previous_symbols[TARGETED_ACCOUNT_UID] = position_result.index.copy()
                is_first_runs[TARGETED_ACCOUNT_UID] = False
                
        time.sleep(300)
    except Exception as e:
        print(f"Error occurred: {e}")
        message                     = f"Error occurred for UID <b>{TARGETED_ACCOUNT_UID}</b>:\n{e}\n\n" \
                                      f"Retrying after 60s"
        telegram_send_message(message)
        time.sleep(60)