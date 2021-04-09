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
5. Startup the database updater
```console
python -m data_handler.database_updater
```
6. Startup the dashboard
```console
python main.py
```
## TODO:

OHLC:

1. Zooming thing works
2. Canvas for drawing
3. Remove date-time for one of the graphs
4. Scaling of volume and MACD
5. Fix 5 mins
6. Beautiful tabs

Market Summary:

1. Putting them in a row.
2. Put the word market summary
3. Color correction
4. Remove zoom/panning functions