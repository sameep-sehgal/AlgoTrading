import requests
import json


endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("keys.json").read())

def positions(symbol=""):
    if len(symbol)>1:
        pos_url = endpoint + "/v2/positions/{}".format(symbol)
    else:
        pos_url = endpoint + "/v2/positions"
    r = requests.get(pos_url, headers=headers)
    return r.json()

positions()


def close_positions(symbol="", qty=0):
    if len(symbol)>1:
        pos_url = endpoint + "/v2/positions/{}".format(symbol)
        params = {"qty" : qty}
    else:
        pos_url = endpoint + "/v2/positions"
        params = {}
    r = requests.delete(pos_url, headers=headers, json=params)
    return r.json()

close_positions("MSFT",1)