# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 15:23:10 2021

@author: samee
"""


import requests
import json

endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("keys.json").read())

def last_trade(symbol):
    last_trade_url = endpoint + '/last/stocks/{}'.format(symbol)
    r=requests.get(last_trade_url,headers=headers)
    return (r.json()["last"]["price"],r.json()["last"]["size"])

last_trade("CSCO")