#!/usr/bin/python3

#=========================================================
# CREATE KEYSPACE and TABLES
#=========================================================

from cassandra.cluster import Cluster
import pandas as pd
from constants import *
from get_binance import *

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

#CREATE KEYSPACE
try:
    print("Creating keyspace")
    session.execute("CREATE KEYSPACE cryptoview WITH replication = {'class':'SimpleStrategy', 'replication_factor': 1}")
except:
    print("Keyspace already created")

session.execute('USE cryptoview')

for symbol in symbols:
    for timeframe in timeframes_detailed:
        try:
            print(f"Creating table {symbol}_{timeframe}")
            session.execute(f"CREATE TABLE {symbol}_{timeframe}({table_column_type})")
        except:
            print(f"Unable to create table {symbol}_{timeframe}")


# EXAMPLE timestamp insertion
# session.execute("insert into test_table (timeframe, int) values ('2021-02-24 00:12:00', 12)")
