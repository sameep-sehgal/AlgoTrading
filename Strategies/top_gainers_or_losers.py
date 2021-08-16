import time
from hist_data_func import hist_data

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