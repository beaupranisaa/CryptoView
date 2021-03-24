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
mkdir <DIRECTORY PATH>
```
3. Run a cassandra container on docker and mount the directory for persistent storage
```console
docker run -d --name cassandra -v <DIRECTORY PATH>:/var/lib/cassandra -p 9042:9042 -p 9160:9160 cassandra
```
4. Initialize the database
```console
python -m data_handler.initialize_database
```
5. Check out the example usage
```console
python -m data_handler.example
```

## TODO:
1. get the latest time on the database and only query the remaining data from binance-spot-api

## Current state:
1. Since save = False in get_all_binance() everytime we run the insert_data command, it re-downloads the data from the binance-api
