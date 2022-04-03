import numpy as np
import pandas as pd
import time
import pyupbit
import datetime
from sys import stdout


INF = 9999999

# def get_crr(df,k,fees):
#     '''
#         df : ohlcv가 들어있는 dataframe
#         k : 변동성 돌파 전략의 k값
#         fees : 매매 수수료
        
#         return df.cumprod[-2]
#     '''
#     #print(df)
#     df['range'] = df['high'].shift(1) - df['low'].shift(1)
#     df['target_price'] = df['open'] + df['range'] * k
#     df['ror_commision'] = np.where(df['high'] > df['target_price'], 
#                          (df['close'] / (1 + fees)) / (df['target_price'] * (1 + fees)), 
#                          1)
#     return df['ror_commision'].cumprod()[-2]

# def old_get_best_k(ticker, count, range_upper, fees):
#     '''
#         ticker : 코인 종목
#         count : BEST K를 구할 때 며칠 전 데이터부터 이용할건지
#         range_upper : k값을 몇 씩 올려가며 테스트해볼건지
#         fees : 수수료
        
#         return best_k
#     '''
#     time.sleep(0.1)
#     to = datetime.datetime.now() + datetime.timedelta(days=-(count))
#     df = pyupbit.get_ohlcv(ticker, interval="day", count=count+1)
#     if df is None:
#         print(ticker, df, INF)
#         return INF

#     max_ror = 0
#     best_k = 0.5
#     for k in np.arange(0.1, 1.0, range_upper):
#         crr = get_crr(df=df, k=k, fees = fees)
#         if crr > max_ror:
#             max_ror = crr
#             best_k = k
    
#     # print("GETTING BEST K : ")
#     # print(df)
#     return best_k

def get_best_k(ticker,count):
    # time.sleep(0.1)
    df = pyupbit.get_ohlcv(ticker=ticker, interval="day", count=count+1)
    if df['high'].shift(1) is df['low'].shift(1):
        return 999999
    df['noise'] = 1 - ( abs(df['open'].shift(1) - df['close'].shift(1)) / (df['high'].shift(1) - df['low'].shift(1)))
    noise_k = df['noise'].mean()
    return noise_k

# def get_mdd(df, mdd_get_days):
#     '''
#         df : ohlcv가 들어있는 dataframe
#         mdd_get_days : mdd를 구할 때 며칠 전부터 현재까지 구할건지
        
#         return None or mdd
#     '''
#     INF = 999999.0
#     if df['ror_commision'] is None:
#         return None
    
#     if len(df) < mdd_get_days:
#         return INF
#     min_ror = INF
#     for i in range(-mdd_get_days, -1, 1):
#         if df['ror_commision'][i] < min_ror:
#             min_ror = df['ror_commision'][i]
#     print(df)
            
#     if min_ror == INF:
#         return None
#     else:
#         return min_ror
    
def get_target_price(ticker, k):
    '''
        ticker : 매매하려는 코인 종듬듬
        df : 매매 코인의 ohlcv
        
        return target_price
    '''
    days_for_best_k = 20
    time.sleep(0.1)
    df = pyupbit.get_ohlcv(ticker) # 새로운 target price를 위해 df를 새로 만듬
    yesterday = df.iloc[-2]
    
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    
    
    target_price = today_open + (yesterday_high - yesterday_low) * k
    
    return target_price

def get_current_price(ticker):
    orderbook = pyupbit.get_orderbook(ticker)
    real_current_price = orderbook['orderbook_units'][0]['ask_price']
    
    return real_current_price

def get_volume(df):
    return df['volume']
def make_df(ticker, count, fees, k):
    '''
        ticker : 거래 코인 종목
        count : 거래 코인 종목의 ohlcv 일수
        fees : 수수료
        k : best_k

        return df
    '''
    df = pyupbit.get_ohlcv(ticker=ticker,count=count)
    df['range'] = df['high'].shift(1)-df['low'].shift(1)
    df['best_k'] = 0.5
    Kchange = True
    for i in range(1, len(df)):
        to = df.index[i]
        df['best_k'][i] = k
    df['target_Price'] = df['open'] + df['range'] * df['best_k']
    df['ror_commision'] = np.where(df['high'] > df['target_Price'], 
                         (df['close'] / (1 + fees)) / (df['target_Price'] * (1 + fees)), 
                         1)
    return df

def get_market_open():
    now = datetime.datetime.now()
    if datetime.datetime.now().hour < 9:
        market_open = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=0, hours=9)
    else:
        market_open = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1, hours=9)
    return market_open

def get_avg_buy_price(ticker, upbit):
    avg_buy_price = None
    balance = upbit.get_balances()
    for i in range(len(balance)):
        if balance[i]['currency'] == ticker.split('-')[1]:
            avg_buy_price = float(balance[i]['avg_buy_price'])
    return avg_buy_price

def isdamage(ticker, upbit, percent):
    avg_buy_price = get_avg_buy_price(ticker=ticker, upbit=upbit)
    current_price = get_current_price(ticker=ticker)
    dmg_percent = (1-(current_price / avg_buy_price))*100
    if dmg_percent > percent:
        return True
    else:
        return False
    
def ismycoin(ticker, upbit):
    balance = upbit.get_balances()
    for i in range(len(balance)):
        if balance[i]['currency'] == ticker.split("-")[1]:
            return True
    return False

def get_my_coin(upbit, no_names):
    '''
        upbit : api 연결 정보
        no_names : 거래하기 싫은 리스트
    '''
    ticker = None
    balance = upbit.get_balances()
    for i in range(len(balance)):
        name = balance[i]['currency']
        if name not in no_names:
            ticker = str("KRW-" + name)
    return ticker

def Update(ticker,upbit):
    K = get_best_k(ticker=ticker, count=20)
    target_price = get_target_price(ticker=ticker, k=K)
    current_price = get_current_price(ticker=ticker)
    avg_buy_price = get_avg_buy_price(ticker=ticker, upbit=upbit)
    market_open = get_market_open()
    
    return K, target_price, current_price, avg_buy_price, market_open
    
def showBuyThings():
    '''
        print ticker that satisfied condition
    '''
    tickers = pyupbit.get_tickers(fiat="KRW")
    #print(tickers)
    right_ticker = []
    right_k = []
    right_current_price = []
    right_target_price = []
    gap_ratio = []
    print("START COLLECTING")
    for index, ticker in list(enumerate(tickers)):
        k = get_best_k(ticker=ticker, count=20)
        target_price = get_target_price(ticker, k)
        current_price = pyupbit.get_current_price(ticker)
        right_ticker.append(ticker)
        right_k.append(k)
        right_current_price.append(current_price)
        right_target_price.append(target_price)
        gap_ratio.append((current_price - target_price) / target_price *100)

        progress = 100 * (index+1) / len(tickers)
        stdout.write("\r{}% DONE, Now : {}".format(progress, ticker))
        stdout.flush()
        
        #dif.append((current_price - target_price)/current_price)
        # print(ticker + " K : " + str(k), end = "")
        # print(" current price : {}, target price : {}".format(current_price , target_price), end="")
        # print(" mdd_30_days : {}".format(get_mdd(df=make_df(ticker=ticker, count = 100,fees=0.005,k=k),mdd_get_days=20)))

    # for ticker in tickers:
    #     target_price = get_target_price(ticker)
    #     current_price = pyupbit.get_current_price(ticker)
    #     if target_price < current_price:
    #         k = get_best_k(ticker=ticker, count=20, range_upper=0.1, fees=0.005)
    #         right_ticker.append(ticker)
    #         right_mdd.append(get_mdd(df=make_df(ticker=ticker, count = 100,fees=0.005,k=k),mdd_get_days=20))
    #         right_k.append(k)
    #         right_current_price.append(current_price)
    #         right_target_price.append(target_price)
    #         # print(ticker + " K : " + str(k), end = "")
    #         # print(" current price : {}, target price : {}".format(current_price , target_price), end="")
    #         # print(" mdd_30_days : {}".format(get_mdd(df=make_df(ticker=ticker, count = 100,fees=0.005,k=k),mdd_get_days=20)))
    stdout.write("\n")
    info_dic={
        #'right_ticker' : right_ticker,
        'right_k' : right_k,
        'right_current_price' : right_current_price,
        'right_target_price' : right_target_price,
        'gap_ratio' : gap_ratio
    }
    indexName = right_ticker
    dataframe = pd.DataFrame(info_dic, indexName)
    dataframe = dataframe.sort_values(by=['gap_ratio'],ascending=False)
    now = datetime.datetime.now()
    dataframe.to_excel("./{}_{}_{}_{}result.xlsx".format(now.month,now.day,now.hour,now.minute))

    return dataframe