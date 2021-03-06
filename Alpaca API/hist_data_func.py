import requests
import json
import pandas as pd
import time


endpoint = "https://data.alpaca.markets/v1"
headers = json.loads(open("keys.json").read())

def hist_data(symbols,timeframe="15Min",limit=200,start="",end="",after="",until=""):
    df_data = {}
    bar_url = endpoint + "/bars/{}".format(timeframe)
    params = {"symbols" : symbols,
          "limit":limit,
          "start":start, "end":end, "after":after,"until":until}
    r = requests.get(bar_url,headers=headers,params=params)
    
    json_dump = r.json()
    
    for sym in json_dump: #Iterate through all symbols is the json_dump dictionary
        temp = json_dump[sym]
        temp = pd.DataFrame(temp) #Create a datafrom for each symbol
        temp.rename({"t":"time","o":"open","h":"high","l":"low","c":"close","v":"volume"},axis=1, inplace=True)
        temp['time'] = pd.to_datetime(temp['time'],unit='s')
        temp.set_index("time",inplace=True)
        temp.index = temp.index.tz_localize("UTC")
        temp.index = temp.index.tz_convert("America/New_York")
        df_data[sym] = temp
    return df_data

if __name__ == "main":
    tickers = ["FB","AMZN","GOOG"]
    starttime = time.time()
    timeout = starttime+60*5 #8hours
    while time.time()<timeout:
        print("**********************")
        for ticker in tickers:
            print("Printing data for {} at {}".format(ticker,time.time()))
            print(hist_data(ticker,timeframe="1Min"))
        time.sleep(60-(time.time()-starttime)%60)
    data_dump = hist_data(symbols="FB,CSCO,AMZN",timeframe="5Min")