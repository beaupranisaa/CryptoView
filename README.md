# CryptoView

## Getting Started:

### DataHandler

1. Install the prerequisites
```console
pip install -r requirements.txt
sudo apt install -y docker
```
2. Create a directory where data will be stored
```console
mkdir ~/storage
```
3. Run a cassandra container on docker and mount the directory for persistent storage
```console
docker run -d --name cassandra -v <DIRECTORY PATH>:/var/lib/cassandra -p 9042:9042 -p 9160:9160 cassandra
```
4. Initialize the database
```console
python initialize_database.py
```
5. Check out the example usage
```console
python example.py
```

## TODO:
1. get the latest time on the database and only query the remaining data from binance-spot-api
2. add more "binsizes" in get_binance currently limited to only {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}

## Current state:
1. Timeframes array in constants.py currently takes only 1h and 1d data
2. Since save = False in get_all_binance() everytime we run the insert_data command, it re-downloads the data from the binance-api
3. 

