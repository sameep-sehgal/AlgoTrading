import websocket
import json
import sqlite3
import datetime


endpoint = "wss://data.alpaca.markets/stream"
headers = json.loads(open("keys.json").read())
streams = ["Q.AAPL","Q.TSLA", "Q.GOOG", "Q.FB","T.AAPL","T.TSLA", "T.GOOG", "T.FB"]


trade_tick_db = sqlite3.connect("./trade_ticks.db") #Connect to a sqllite DB
quote_tick_db = sqlite3.connect("./quote_ticks.db")


def return_tickers(streams, tick_type="T"):
    #Used to extract tickers of particular stream tick_type: Trade(T) or Quote(Q)
    tickers = []
    for stream in streams:
        stream_tick_type,stream_ticker = stream.split(".")
        if(stream_tick_type == tick_type and stream_ticker not in tickers):
            tickers.append(stream_ticker)
    return tickers


def create_tables(tickers, db, tick_type="T"):
    cur = db.cursor() #Cursor to the SQLite DB. this will be used to make changes to DB
    if tick_type == "T":
        for ticker in tickers:
            cur.execute("CREATE TABLE IF NOT EXISTS {} (timestamp datetime primary key, price real(15,5), volume integer)".format(ticker))
    
    if tick_type == "Q":
        for ticker in tickers:
            cur.execute("CREATE TABLE IF NOT EXISTS {} (timestamp datetime primary key, bid_price real(15,5), bid_volume integer, ask_price real(15,5), ask_volume integer)".format(ticker))
    try:
        db.commit()
    except:
        db.rollback()

create_tables(return_tickers(streams,"T"),trade_tick_db,"T")
create_tables(return_tickers(streams,"Q"),quote_tick_db,"Q")
#cur.execute('SELECT name from sqlite_master where type="table"')
#cur.fetchall()


def insert_tick(tick):
    if tick["stream"].split(".")[0] == "T":
        cur = trade_tick_db.cursor()
    
        for ms in range(100): #Add few ms to time when alpaca returns duplicate timestamps as timestamp is primary key
            try:
                table_name = tick['stream'].split('.')[-1]
                vals = [datetime.datetime.fromtimestamp(int(tick['data']['t'])/10**9)+datetime.timedelta(milliseconds=ms)
                        ,tick['data']['p'],
                        tick['data']['s']]
                query = "INSERT INTO {} (timestamp,price,volume) VALUES (?,?,?)".format(table_name)
                cur.execute(query,vals) #Return an error if duplicate timestamp is tried to be inserted
                break #Break out of loop as soon as we get unique timestamp which is inserted in DB successfully
            except Exception as e:
                print(e)
        
        try:
            trade_tick_db.commit()
        except:
            trade_tick_db.rollback()
    
    if tick["stream"].split(".")[0] == "Q":
        cur = quote_tick_db.cursor()
    
        for ms in range(100): #Add few ms to time when alpaca returns duplicate timestamps as timestamp is primary key
            try:
                table_name = tick['stream'].split('.')[-1]
                vals = [datetime.datetime.fromtimestamp(int(tick['data']['t'])/10**9)+datetime.timedelta(milliseconds=ms)
                        ,tick['data']['p'],
                        tick['data']['s']
                        ,tick['data']['P'],
                        tick['data']['S']]
                query = "INSERT INTO {} (timestamp,bid_price,ask_price,bid_volume,ask_volume) VALUES (?,?,?,?,?)".format(table_name)
                cur.execute(query,vals) #Return an error if duplicate timestamp is tried to be inserted
                break #Break out of loop as soon as we get unique timestamp which is inserted in DB successfully
            except Exception as e:
                print(e)
        
        try:
            quote_tick_db.commit()
        except:
            quote_tick_db.rollback()

def on_open(ws):
    #Callback function when connection with server opens
    auth = {
            "action": "authenticate",
            "data": {
                "key_id": headers["APCA-API-KEY-ID"],
                "secret_key": headers["APCA-API-SECRET-KEY"]
            }
        }
    #Sending authentication details
    ws.send(json.dumps(auth))#Convert JSON to string(Requirement of Alpaca)
    message = {
            "action": "listen",
            "data": {
                "streams": streams
                }
            }    
    #Sending the channels to join for steaming
    ws.send(json.dumps(message))#Convert JSON to string


def on_message(ws,message):
    #Callback function that runs each time server sends some message to client
    print(message)
    tick = json.loads(message) #Alpaca returns a string which we need to convert to dictionary
    #Store tick data in our DB
    insert_tick(tick)
    
    

def on_close(ws):
    print("Connection Closed")
    
ws = websocket.WebSocketApp(endpoint,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()
