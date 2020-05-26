import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import pandas_datareader.data as web
import yfinance as yf

ibov = yf.download(tickers = '^BVSP')[['Adj Close']]

ibov.plot(figsize = (22,8), label = "IBOV")
ibov.rolling(21).mean().plot(label = 'MM21')
ibov.rolling(200).mean().plot(label = 'MM200')
plt.legend()
plt.show()