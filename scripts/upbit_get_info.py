import numpy as np
import time
import pyupbit
import datetime

def get_crr(df,k,fees):
    '''
        df : ohlcv가 들어있는 dataframe
        k : 변동성 돌파 전략의 k값
        fees : 매매 수수료
        
        return df.cumprod[-2]
    '''
    df['range'] = df['high'].shift(1) - df['low'].shift(1)
    df['target_price'] = df['open'] + df['range'] * k
    df['ror_commision'] = np.where(df['high'] > df['target_price'], 
                         (df['close'] / (1 + fees)) / (df['target_price'] * (1 + fees)), 
                         1)
    return df['ror_commision'].cumprod()[-2]

def get_best_k(ticker, count, range_upper, fees):
    '''
        ticker : 코인 종목
        count : BEST K를 구할 때 며칠 전 데이터부터 이용할건지
        range_upper : k값을 몇 씩 올려가며 테스트해볼건지
        fees : 수수료
        
        return best_k
    '''
    to = datetime.datetime.now() + datetime.timedelta(days=-(count))
    df = pyupbit.get_ohlcv(ticker, to=to, interval="day", count=count+1)
    time.sleep(0.05)
    max_ror = 0
    best_k = 0.5
    for k in np.arange(0.1, 1.0, range_upper):
        crr = get_crr(df=df, k=k, fees = fees)
        if crr > max_ror:
            max_ror = crr
            best_k = k
    
    return best_k

def get_mdd(df, mdd_get_days):
    '''
        df : ohlcv가 들어있는 dataframe
        mdd_get_days : mdd를 구할 때 며칠 전부터 현재까지 구할건지
        
        return None or mdd
    '''
    INF = 999999.0
    if df['ror_commision'] is None:
        return None
    min_ror = INF
    for i in range(-mdd_get_days, -1, 1):
        if df['ror_commision'][i] < min_ror:
            min_ror = df['ror_commision'][i]
            
    if min_ror == INF:
        return None
    else:
        return min_ror
    
def get_target_price(ticker):
    '''
        ticker : 매매하려는 코인 종듬듬
        df : 매매 코인의 ohlcv
        
        return target_price
    '''
    days_for_best_k = 20
    
    df = pyupbit.get_ohlcv(ticker) # 새로운 target price를 위해 df를 새로 만듬
    yesterday = df.iloc[-2]
    
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    
    k = get_best_k(ticker = ticker, count = days_for_best_k,
                   range_upper=0.1, fees = 0.0005)
    
    target_price = today_open + (yesterday_high - yesterday_low) * k
    
    return target_price

def get_current_price(ticker):
    orderbook = pyupbit.get_orderbook(ticker)
    real_current_price = orderbook['orderbook_units'][0]['ask_price']
    
    return real_current_price
    
def make_df(ticker, count, fees, k):
    '''
        ticker : 거래 코인 종목
        count : 거래 코인 종목의 ohlcv 일수
        fees : 수수료
        k : best_k
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
    df['target_price_with_0.5'] = df['open'] + df['range']*0.5
    df['ror_commision_with_0.5'] = np.where(df['high'] > df['target_price_with_0.5'], 
                                   (df['close'] / (1 + fees)) / (df['target_price_with_0.5'] * (1 + fees)), 
                                   1)
    return df