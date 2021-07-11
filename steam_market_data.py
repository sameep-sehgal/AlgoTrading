# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 09:01:51 2021

@author: samee
"""

import websocket
import json
import sqlite3
import datetime


endpoint = "wss://data.alpaca.markets/stream"
headers = json.loads(open("keys.json").read())
streams = ["T.AAPL","T.TSLA", "Q.GOOG", "T.FB"]


db = sqlite3.connect("./ticks.db") #Connect to a sqllite DB
cur = db.cursor() #Cursor to the SQLite DB. this will be used to make changes to DB

def create_tables(tickers):
    for ticker in tickers:
        cur.execute("CREATE TABLE IF NOT EXISTS {} (timestamp datetime primary key, price real(15,5), volume integer)".format(ticker))
    try:
        db.commit()
    except:
        db.rollback()

create_tables([i.split(".")[1] for i in streams])
cur.execute('SELECT name from sqlite_master where type="table"')
cur.fetchall()

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
        db.commit()
    except:
        db.rollback()
    

def on_close(ws):
    print("Connection Closed")
    
ws = websocket.WebSocketApp(endpoint,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()
