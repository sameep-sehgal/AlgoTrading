import requests
import os
import json

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("keys.json").read())


def market_order(symbol, quantity, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "market",
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()

market_order("AMZN", 1) 


def limit_order(symbol, quantity, limit_pr, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "limit",
              "limit_price" : limit_pr,
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()


def stop_order(symbol, quantity, stop_pr, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "stop",
              "stop_price": stop_pr,
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()


stop_order("AMZN", 1, 3185, "sell")

def stop_limit_order(symbol, quantity, stop_pr, limit_pr, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "stop_limit",
              "stop_price": stop_pr,
              "limit_price" : limit_pr,
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()


def trail_stop_order(symbol, quantity, trail_pr, side="buy", tif="day"):
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "trailing_stop",
              "trail_price" : trail_pr,
              "time_in_force": tif}
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()
  
limit_order("AMZN", 1, limit_pr = 3202)

