import time
from data_handler.data_handler import DataHandler

dh = DataHandler()

def update_database():
    print("Updating Database")
    dh.insert_all_data()

while True:
    update_database()
    time.sleep(60)