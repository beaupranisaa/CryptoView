#!/usr/bin/python3

from cassandra.cluster import Cluster
import pandas as pd
from constants import *
from get_binance import *

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute('USE cryptoview')

get_what = 'get_historical_klines'
full_data, new_data = get_all_binance(get_what, "BTCUSDT", '1h', save=True)

a_data = full_data.iloc[0,:].values
print(a_data)

insert_string = f"'{full_data.iloc[0,5]}', "
insert_string2 = ''

for i,data in enumerate(a_data):
    if i == 5:
        insert_string += "'"
    string_data = str(data)
    insert_string += string_data
    if i == 5:
        insert_string += "'"
    insert_string += ', '

insert_string = insert_string[:-2]

session.execute(f"INSERT INTO btcusdt_1hour({table_column}) VALUES ({insert_string})")
