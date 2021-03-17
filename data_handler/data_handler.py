#!/usr/bin/python3

from cassandra.cluster import Cluster
import pandas as pd
from constants import *
from get_binance import *
from tqdm import tqdm

class DataHandler:
    def __init__(self):
        cluster = Cluster(['puffer.cs.ait.ac.th'])
        self.session = cluster.connect()
        try:
            self.session.execute('USE cryptoview')
        except:
            self.initialize_database()

        # TODO: get the lastest timestamp of the database for each of the coins.

    def initialize_database(self):
        #CREATE KEYSPACE
        try:
            print("Creating keyspace")
            self.session.execute("CREATE KEYSPACE cryptoview WITH replication = {'class':'SimpleStrategy', 'replication_factor': 1}")
        except:
            print("Keyspace already created")

        self.session.execute('USE cryptoview')

        for symbol in tqdm(symbols):
            self.session.execute(f"CREATE TABLE {symbol}(timeframe text, {table_column_type}, PRIMARY KEY (timeframe, timestamp))") 

    def insert_data(self, symbol, timeframe):
        get_what = 'get_historical_klines'

        full_data, new_data = get_all_binance(get_what, symbol, timeframe, save=False)

        for index, row in tqdm(list(full_data.iterrows())):
            values_string = f"'{index}', "

            for i, value in enumerate(row.values):
                if i == 5:
                    values_string += "'"
                values_string += str(value)
                if i == 5:
                    values_string += "'"
                values_string += ', '
            values_string = values_string[:-2]

            query_string = f"INSERT INTO {symbol}(timeframe, {table_column}) VALUES ('{timeframes_detailed[timeframes.index(timeframe)]}', {values_string})"

            self.session.execute(query_string)

    def insert_all_data(self):
        for s in symbols:
            for t in timeframes:
                self.insert_data(s,t)

    def get_data(self, symbol, timeframe, range=None):
        '''
        range = [start_time, end_time] 
        examples:
        range = ['2017-02-20','2019-02-20'] -> from 2017-02-20 to 2019-02-20
        range = [None,'2019-02-20'] -> from start to 2019-02-20
        range = ['2017-02-20',None] -> from 2017-02-20 to now
        range = [None,None] ->  all data
        range = None ->  all data
        '''
        table = f"{symbol}"

        if range == None or (range[0] == None and range[1] == None):
            data = self.session.execute(f"select * from {table} where timeframe = '{timeframes_detailed[timeframes.index(timeframe)]}'")
        elif range[0] == None:
            data = self.session.execute(f"select * from {table} where timeframe = '{timeframes_detailed[timeframes.index(timeframe)]}' and timestamp <= '{range[1]}'")
        elif range[1] == None:
            data = self.session.execute(f"select * from {table} where timeframe = '{timeframes_detailed[timeframes.index(timeframe)]}' and timestamp >= '{range[0]}'")
        else:
            data = self.session.execute(f"select * from {table} where timeframe = '{timeframes_detailed[timeframes.index(timeframe)]}' and timestamp >= '{range[0]}' and timestamp <= '{range[1]}'")

        data = pd.DataFrame(data)

        if data.size == 0:
            return None

        data.set_index('timestamp', inplace=True)
        return data

if __name__ == "__main__":

    datahandler = DataHandler()

    #datahandler.insert_data('ETHUSDT', '1d')
    datahandler.insert_all_data()
