import numpy as np
from talib import abstract


# from talib.abstract import SMA
# note that all ndarrays must be the same length!

def example1():
    inputs = {
        'open': np.random.random(100),
        'high': np.random.random(100),
        'low': np.random.random(100),
        'close': np.random.random(100),
        'volume': np.random.random(100)
    }

    # print(inputs)
    sma = abstract.SMA
    ##sma = abstract.Function('sma')

    macd  = abstract.MACD

    output_default = sma(inputs, timeperiod=20)  # calculate on close prices by default
    output_open = sma(inputs, timeperiod=20, price='open')  # calculate on opens

    # upper, middle, lower = BBANDS(input_arrays, 20, 2, 2)
    # slowk, slowd = STOCH(input_arrays, 5, 3, 0, 3, 0)  # uses high, low, close by default
    # slowk, slowd = STOCH(input_arrays, 5, 3, 0, 3, 0, prices=['high', 'low', 'open'])

    #print(output_default)
    # print(output_open)

    macd_result = macd(inputs, fastperiod=12, slowperiod=26, signalperiod=9)
    #macd, macdsignal, macdhist
    print(macd_result[0])

if __name__ == '__main__':
    example1()
