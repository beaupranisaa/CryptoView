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
