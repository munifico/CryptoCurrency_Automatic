import pyupbit
import time
import datetime
import backtesting
import numpy as np
fees = 0.0005  
access_key = None
secret_key = None
with open("pyupbit_key.txt") as f:
    lines = f.readlines()
    access_key = lines[0].strip()
    secret_key = lines[1].strip()
upbit = pyupbit.Upbit(access_key, secret_key)

days_for_best_k = 21
# 2. 목표가 계산하기

def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2] 

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    
    
    to = datetime.datetime.now() + datetime.timedelta(days=-(days_for_best_k-1))
    k = get_best_K(to=to, ticker=ticker)
    
    target_price = today_open + (yesterday_high - yesterday_low) * k

    return target_price

# 4. 매수 시도하기

def buy_crypto_currency(ticker):
    krw = upbit.get_balance(ticker="KRW")
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook['orderbook_units'][0]['ask_price']
    unit = krw / (float(sell_price))
    if(sell_price * unit >= 5000):
        print("buy")
        #upbit.buy_limit_order(ticker, sell_price, unit-1)
        ret = upbit.buy_market_order(ticker, krw*0.9995)
        print(ret)
        print_info(ticker)
    
    

# 1. 주기적으로 현재가 얻어오기
# 3. 09:00 에 목표가 갱신하기

# 5. 매도 시도하기
def sell_crypto_currency(ticker):
    print("SELL CRYPTO")
    unit = upbit.get_balance(ticker)
    ret = upbit.sell_market_order(ticker=ticker, volume=unit)
    print(ret)
    print("판매 개수 : " + str(unit))
    print("SOLD OUT")
    print_info(ticker)

def print_info(ticker):
    now = datetime.datetime.now()
    target_price = get_target_price(ticker)
    current_price = pyupbit.get_current_price(ticker)
    to = datetime.datetime.now() + datetime.timedelta(days=-(days_for_best_k-1))
    k = get_best_K(to=to, ticker=ticker)
    print("TICKER : " + str(ticker))
    print("현재 시간 : "  + str(now))
    print("BEST K : " + str(k))
    print("target price : " + str(target_price))
    print("current price : " + str(current_price))
    print("현재 KRW : " + str(upbit.get_balance("KRW")))
    print("현재 ticker : " + str(upbit.get_balance(ticker)))

# 최적의 K 구하기
def get_crr(df, K):
    try:
        df['range'] = df['high'].shift(1)-df['low'].shift(1) # 전날 고가 - 저가
        df['target_price'] = df['open'] + df['range'] * K
        df['ror_commision'] = np.where(df['high'] > df['target_price'], 
                         (df['close'] / (1 + fees)) / (df['target_price'] * (1 + fees)), 
                         1)
        return df['ror_commision'].cumprod()[-2]
    except:
        print("error : ")
        return None

def get_best_K(to, ticker):
    if to is None:
        to = datetime.datetime.now() + datetime.timedelta(days=-(days_for_best_k-1))
    df = pyupbit.get_ohlcv(ticker, to=to, interval="day", count=days_for_best_k)
    time.sleep(0.05)
    max_ror = 0
    best_K = 0.5
    for k in np.arange(0.1, 1.0, 0.1):
        crr = get_crr(df=df,K=k)
        if crr is None:
            return None
        if crr > max_ror:
            max_ror = crr
            best_K = k
            
    return best_K
####

# 실행 #
def run(ticker):
    now = datetime.datetime.now()
    market_open = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1,hours=9)
    print("market_open : " + str(market_open))
    target_price = get_target_price(ticker)
    current_price = pyupbit.get_current_price(ticker)
    print_info(ticker)
    while True:
        now = datetime.datetime.now()
        target_price = get_target_price(ticker)
        current_price = pyupbit.get_current_price(ticker)
        if market_open < now < market_open + datetime.timedelta(seconds=10):
            target_price = get_target_price(ticker)
            print("갱신된 target price : " + str(target_price))
            market_open = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1,hours=9)
            print_info(ticker)
            sell_crypto_currency(ticker)

        if now.minute == 0 and 0 < now.second < 3:
            to = datetime.datetime.now() + datetime.timedelta(days=-(days_for_best_k-1))
            k = get_best_K(to=to, ticker=ticker)
            print("현재 시간 : " + str(now), end="")
            print(" BEST K : " + str(k))
        if target_price < current_price:
            ret = buy_crypto_currency(ticker)
            if ret is not None:
                print(ret)

        time.sleep(1)
        
def showBuyThings():
    print("!!")
    tickers = pyupbit.get_tickers(fiat="KRW", )
    print(tickers)
    for ticker in tickers:
        target_price = get_target_price(ticker)
        current_price = pyupbit.get_current_price(ticker)
        if target_price < current_price:
            k = get_best_K(to=None, ticker=ticker)
            if k is None:
                print(ticker)
            else:                
                print(ticker + " K : " + str(k), end = "")
                print(" current price : {}, target price : {}".format(current_price , target_price), end="")
                print(" mdd_30_days : {}".format(backtesting.get_mdd(df=backtesting.make_df(ticker=ticker, count = 100))))
            

if __name__ == '__main__':
    #showBuyThings()
    run("KRW-ARK")
    