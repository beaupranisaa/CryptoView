#!/usr/bin/python3

from data_handler.data_handler import DataHandler

# Create a data handler
dh = DataHandler()

# Insert data into database
dh.insert_data('ETHUSDT', '1d')

'''
# Insert all data
dh.insert_all_data()
'''

# query data from the range '2020-01-30' to '2020-02-02' 
data = dh.get_data('ETHUSDT','1d',['2020-01-30','2020-02-02'])

# returns a pandas dataframe
print(data)


