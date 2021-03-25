# IMPORTS
#%%

# REFERENCE : https://medium.com/swlh/retrieving-full-historical-data-for-every-cryptocurrency-on-binance-bitmex-using-the-python-apis-27b47fd8137f

import pandas as pd
import math
import os.path
import time
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm_notebook #(Optional, used for progress-bars)

# CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440} # if you need other time frame : key = timeframe, value = minutes
batch_size = 750

binance_api_key = 'mH1tBFKTHPe8ghyXi5YUTNsk5xdFdltSDGa6B7ILjmpOczqYbEl59ij4awjbshHE'    #Enter your own API-key here
binance_api_secret = 'Gkaspu0Ol4xnWjVFQR7PlYpmqwCKckxI3zAy6loVE8Ub80kwH0x18ENCujav0Xzm' #Enter your own API-secret here

binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

### FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source): #get the datetime of oldest and latest data we have
    if len(data) > 0:  
        old = parser.parse(data["timestamp"].iloc[-1])
    else:
        old = datetime.strptime('1 Jan 2017', '%d %b %Y')

    new     = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    return old, new


def get_all_binance(get_what, symbol, timeframe, start_time=None):

    if start_time == None: 
        oldest_point = datetime.strptime('1 Jan 2017','%d %b %Y').strftime('%d %b %Y %H:%M:%S')
    else:
        oldest_point = start_time.strftime('%d %b %Y %H:%M:%S')
    newest_point = datetime.now().strftime('%d %b %Y %H:%M:%S')

    print(f'Downloading {symbol}_{timeframe} data from {oldest_point} to {newest_point}')

    klines = getattr(binance_client, get_what)(symbol, timeframe, oldest_point, newest_point)

    #this stores the latest data
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms').astype('datetime64[s]')
    data['close_time'] = pd.to_datetime(data['timestamp'], unit='ms').astype('datetime64[s]')
    
    data.set_index('timestamp', inplace=True)
    
    print('All caught up..!')

    return data

if __name__ == "__main__":
    # see all possible get what here : https://python-binance.readthedocs.io/en/latest/binance.html
    get_what = 'get_historical_klines'

    # Top 10 coins by market cap
    #binance_symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "USDTUSDT", "XTZUSDT", "BSVUSDT", "LTCUSDT", "EOSUSDT", "BNBUSDT", "BCHUSDT"]
    #for symbol in reversed(binance_symbols):
    #    get_all_binance(get_what, symbol, '1h', save = True)

    get_all_binance(get_what, "BTCUSDT", '1h')

# 1. tether
# 2. BSVUSDT
# 3. Dogecoin (
