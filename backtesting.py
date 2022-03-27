import pyupbit
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
fees = 0.0005
def draw_chart(df, ticker, day=None):
    #plt.plot(df['date'], df['profit_for_graph'])
    #plt.plot(df['date'], df['close'])
    if day is None:
        day = len(df)
    plt.figure(figsize=(11,7))
    plt.plot(df['close'], label=str(ticker)+" PRICE")
    plt.plot(df['profit_for_graph'], label="PROFIT RATE")
    plt.xlabel("DATE")
    plt.ylabel("WON")
    plt.legend(loc=2)
    
    plt.title("Graph of "+str(ticker)+" ("+str(day)+"days)")
    plt.savefig("chart/"+str(ticker)+"_" + str(day) +".png")
    
def get_crr(df, K):
    df['range'] = df['high'].shift(1)-df['low'].shift(1) # 전날 고가 - 저가
    df['target_price'] = df['open'] + df['range'] * K
    df['ror_commision'] = np.where(df['high'] > df['target_price'], 
                         (df['close'] / (1 + fees)) / (df['target_price'] * (1 + fees)), 
                         1)
    return df['ror_commision'].cumprod()[-2]

def get_best_K(to, ticker):
    df = pyupbit.get_ohlcv(ticker, to=to, interval="day", count=21)
    time.sleep(0.05)
    max_ror = 0
    best_K = 0.5
    for k in np.arange(0.1, 1.0, 0.1):
        crr = get_crr(df=df,K=k)
        if crr > max_ror:
            max_ror = crr
            best_K = k
            
    return best_K

def make_df(ticker, count):
    df = pyupbit.get_ohlcv(ticker=ticker,count=count)
    df['range'] = df['high'].shift(1)-df['low'].shift(1)
    df['best_k'] = 0.5
    Kchange = True
    for i in range(1, len(df)):
        to = df.index[i]
        if len(df) < count :
            k = 0.5
            Kchange = False
        else:
            k = get_best_K(to=to, ticker=ticker) # 직접 만든 df 사용
        df['best_k'][i] = k
    df['target_Price'] = df['open'] + df['range'] * df['best_k']
    df['ror_commision'] = np.where(df['high'] > df['target_Price'], 
                         (df['close'] / (1 + fees)) / (df['target_Price'] * (1 + fees)), 
                         1)
    df['target_price_with_0.5'] = df['open'] + df['range']*0.5
    df['ror_commision_with_0.5'] = np.where(df['high'] > df['target_price_with_0.5'], 
                                   (df['close'] / (1 + fees)) / (df['target_price_with_0.5'] * (1 + fees)), 
                                   1)
    return df
def get_mdd(df):
    if df['ror_commision'] is None:
        return None
    min_ror = 100.0
    for i in range(-30,-1,1):
        if df['ror_commision'][i] < min_ror:
            min_ror = df['ror_commision'][i]
            
    if min_ror == 100.0:
        return None
    else:
        return min_ror
    
def backtest(ticker, count):
    '''
        target 형식은 df['open'], df['close'], df['high'], df['low']의 형식이어야 함.
    '''
    df =make_df(ticker=ticker, count=count)
    
    Kchange = True
    if len(df) < count :
        k = 0.5
        Kchange = False
        
    print("mdd_30 days : {}".format(get_mdd(df=df)))
    df.to_excel("xls/NEW "+str(ticker)+"_" + str(count) +".xlsx")
    if not Kchange: print("K = 0.5 ", end="")
    print(str(ticker) + " " + str(len(df)) + "days total_ror : " + 
          str(df['ror_commision'].cumprod()[-2]) + " MDD : " + str(df['ror_commision'].min()) + 
         " 0.5_ror : " + str(df['ror_commision_with_0.5'].cumprod()[-2])
          + " MDD_with_0.5 : "+str(df['ror_commision_with_0.5'].min()))
    #draw_chart(df,ticker=ticker)
    
if __name__=="__main__":
    # tickers = ["KRW-ETC", "KRW-BTC", "KRW-EOS", "KRW-BTC", "KRW-ETH", "KRW-XRP"]
    # counts = [365]
    # result = []
    # for ticker in tickers:
    #     for count in counts:
    #         result.append(backtest(ticker=ticker, count=count))
    backtest(ticker="KRW-ARK", count=100)
    #backtest(ticker="KRW-AXS", count=365)
    #backtest(ticker="KRW-ETC", count=4800)
