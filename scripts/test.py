import pyupbit
import numpy as np

def backtest(count):
    df = pyupbit.get_ohlcv("KRW-BTC", count=count)
    df['range'] = (df['high']-df['low'])*0.5
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close']/df['target'],
                         1)

    df['ror_commision'] = np.where(df['high'] > df['target'],
                                   (df['close']/df['target'])*pow(0.9995,2),
                                   1)
    df['ror_commision_cumprod'] = df['ror_commision'].cumprod()
    df['profit_for_graph'] = df['close'][0] * df['ror_commision_cumprod']
    #df.to_excel("test.xlsx")
    print(df.iloc[:,1])
    
backtest(20)