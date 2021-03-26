#!/usr/bin/python3

from cassandra.cluster import Cluster
import pandas as pd
from tqdm import tqdm

from data_handler.constants import *
from data_handler.get_binance import get_all_binance

class DataHandler:
    def __init__(self):
        cluster = Cluster(['puffer.cs.ait.ac.th'])
        self.session = cluster.connect()
        try:
            self.session.execute('USE cryptoview')
        except:
            self.initialize_database()

    def initialize_database(self):
        #CREATE KEYSPACE
        try:
            print("Creating keyspace")
            self.session.execute("CREATE KEYSPACE cryptoview WITH replication = {'class':'SimpleStrategy', 'replication_factor': 1}")
        except:
            print("Keyspace already created")

        table_column_type = ''
        for feature, feature_type in zip(features,features_types):
            table_column_type += feature
            table_column_type += " "
            table_column_type += feature_type
            table_column_type += ", "
        table_column_type = table_column_type [:-2]

        self.session.execute('USE cryptoview')

        for symbol in tqdm(symbols):
            self.session.execute(f"CREATE TABLE {symbol}(timeframe text, {table_column_type}, PRIMARY KEY (timeframe, timestamp))") 

    def insert_data(self, symbol, timeframe):
        get_what = 'get_historical_klines'

        start_time = self.get_latest_timestamp(symbol,timeframe)

        full_data = get_all_binance(get_what, symbol, timeframe, start_time)

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

            table_column = ''
            for feature in features:
                table_column += feature
                table_column += ', '
            table_column = table_column[:-2]

            query_string = f"INSERT INTO {symbol}(timeframe, {table_column}) VALUES ('{timeframes_detailed[timeframes.index(timeframe)]}', {values_string})"

            self.session.execute(query_string)

    def insert_all_data(self):
        for s in symbols:
            for t in timeframes:
                self.insert_data(s,t)

    def get_data(self, symbol, timeframe, range=None, limit = None):
        '''
        range = [start_time, end_time] 
        examples:
        range = ['2017-02-20','2019-02-20'] -> from 2017-02-20 to 2019-02-20
        range = [None,'2019-02-20'] -> from start to 2019-02-20
        range = ['2017-02-20',None] -> from 2017-02-20 to now
        range = [None,None] ->  all data
        range = None ->  all data
        '''

        if limit != None:
            limit_string = f"limit {limit}"
        else:
            limit_string = ""

        if range == None or (range[0] == None and range[1] == None):
            data = self.session.execute(f"select * from {symbol} where timeframe = '{timeframes_detailed[timeframes.index(timeframe)]}' order by timestamp desc {limit_string}")
        elif range[0] == None:
            data = self.session.execute(f"select * from {symbol} where timeframe = '{timeframes_detailed[timeframes.index(timeframe)]}' and timestamp <= '{range[1]}' order by timestamp desc {limit_string}")
        elif range[1] == None:
            data = self.session.execute(f"select * from {symbol} where timeframe = '{timeframes_detailed[timeframes.index(timeframe)]}' and timestamp >= '{range[0]}' order by timestamp desc {limit_string}")
        else:
            data = self.session.execute(f"select * from {symbol} where timeframe = '{timeframes_detailed[timeframes.index(timeframe)]}' and timestamp >= '{range[0]}' and timestamp <= '{range[1]}' order by timestamp desc {limit_string}")

        data = pd.DataFrame(data)

        if data.size == 0:
            return None

        data.set_index('timestamp', inplace=True)
        return data
    
    def get_latest_timestamp(self, symbol, timeframe):
        '''
        Returns latest timestamp (datetime) of a symbol+timeframe
        '''
        timestamp = self.session.execute(f"select timestamp from {symbol} where timeframe = '{timeframes_detailed[timeframes.index(timeframe)]}' order by timestamp desc limit 1")
        return next(iter(timestamp)).timestamp

if __name__ == "__main__":

    datahandler = DataHandler()

    #datahandler.insert_data('ETHUSDT', '1d')
    datahandler.insert_all_data()