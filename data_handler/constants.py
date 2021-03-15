symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "XTZUSDT", "LTCUSDT", "EOSUSDT", "BNBUSDT", "BCHUSDT"]
#timeframes = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
timeframes = ['1h', '1d']
#timeframes_detailed = ['1min', '3min', '5min', '15min', '30min', '1hour', '2hour', '4hour', '6hour', '8hour', '12hour', '1day', '3day', '1week', '1month']
timeframes_detailed = ['1hour', '1day']
features = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore']
features_types = ['TIMESTAMP', 'FLOAT', 'FLOAT', 'FLOAT', 'FLOAT', 'FLOAT', 'TIMESTAMP', 'FLOAT', 'INT', 'FLOAT', 'FLOAT', 'FLOAT']

table_column_type = ''
for feature, feature_type in zip(features,features_types):
    table_column_type += feature
    table_column_type += " "
    table_column_type += feature_type
    table_column_type += ", "
table_column_type = table_column_type [:-2]

table_column = ''
for feature in features:
    table_column += feature
    table_column += ', '
table_column = table_column[:-2]
