import requests
import json
import pandas as pd

endpoint = "https://paper-api.alpaca.markets"
headers = json.loads(open("keys.json").read())


def get_orders(status="open",limit=50):
    #Returns a dataframe of all orders of status = status
    ord_url = endpoint + "/v2/orders"
    params = {"status":status}
    r=requests.get(ord_url,headers=headers,params=params)
    data = r.json()
    return pd.DataFrame(data)

order_df = get_orders()


def market_order(symbol, quantity, side="buy", tif="day"):
    #Places a market order
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
    #Places a limit order
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
    #Places a stop order
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


trail_stop_order("FB",5,2,"sell")


def bracket_order(symbol, quantity,tplp,slsp,sllp, side="buy", tif="day"):
    #Places 3 orders 1Entry and 2Exit{takeProfit and stopLoss}
    #Exit orders are places only when entry orders are filled
    ord_url = endpoint + "/v2/orders"
    params = {"symbol": symbol,
              "qty": quantity,
              "side" : side,
              "type": "market",
              "time_in_force": tif,
              "order_class":"bracket",
              "take_profit":{
                  "limit_price":tplp
                },
              "stop_loss":{
                  "stop_price":slsp,
                  "limit_price":sllp
                }
              }
    r = requests.post(ord_url, headers=headers, json=params)
    return r.json()
  
bracket_order("AAPL", 1, 150, 143, 142.5)

#Get order_id by : order_df[order_df['symbol']=='MSFT']['id'].to_list()[0]

def cancel_order(order_id=""):
    #Cancels all open orders if no argument is provided else cancels only 1 order
    ord_url = endpoint + "/v2/orders"
    ord_url = endpoint + "/v2/orders/{}".format(order_id) if len(order_id) else ord_url
    requests.delete(ord_url, headers=headers)
    
    
def modify_order(params,order_id=""):
    #Replaces original order with a new order with modified parameters
    ord_url = endpoint + "/v2/orders/{}".format(order_id)
    r = requests.patch(ord_url, headers=headers,json=params)
    return r.json()


modify_order({"qty":10,"trail":3},order_df[order_df["symbol"]=="FB"]["id"].to_list()[0])
cancel_order(order_df[order_df['symbol']=='MSFT']['id'].to_list()[0])

