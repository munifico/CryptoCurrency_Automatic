from re import U
import upbit_buy_and_sell
import upbit_get_info
import upbit_print
import account_keys
import pyupbit
import datetime
import time

access_key, secret_key = account_keys.get_keys()
upbit = pyupbit.Upbit(access=access_key, secret=secret_key)

FEE = 0.0005
def run(ticker):
    print("NOW TICKER : {}".format(ticker))
    best_k = upbit_get_info.get_best_k(ticker=ticker, count=20, range_upper=0.1, fees=FEE)
    time.sleep(0.5)
    df = upbit_get_info.make_df(ticker=ticker, count=365, fees=FEE, k=best_k)
    
    now = datetime.datetime.now()
    
    if datetime.datetime.now().hour < 9:
        market_open = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=0,hours=9)
    else:
        market_open = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1,hours=9)
    upbit_print.print_info(ticker = ticker, df=df, k=best_k, market_open=market_open)
    
    target_price = upbit_get_info.get_target_price(ticker=ticker, k = best_k)
    current_price = upbit_get_info.get_current_price(ticker=ticker)
    
    while True:
        now = datetime.datetime.now()
        if market_open < now < market_open + datetime.timedelta(seconds=10):
            target_price = upbit_get_info.get_target_price(ticker=ticker, k=best_k)
            great_ticker = upbit_get_info.showBuyThings()
            great_ticker = great_ticker.index[0]
            ticker = great_ticker   
            print("갱신된 NOW TICKER : {}".format(ticker))
            print("갱신된 target price : " + str(target_price))
            market_open = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1,hours=9)
            upbit_print.print_info(ticker=ticker, df=df, k=best_k, market_open=market_open)
            upbit_buy_and_sell.sell_crypto_currency(ticker=ticker, unit = upbit.get_balance(ticker))
            time.sleep(1)
            print("start making xlsx")
            upbit_get_info.showBuyThings()
            print("done")
            
        # if now.minute == 0 and 0 < now.second < 3:
        if 0 < now.second < 3:
            best_k = upbit_get_info.get_best_k(ticker = ticker, count = 20, range_upper=0.1, fees=FEE)
            time.sleep(0.5)
            target_price = upbit_get_info.get_target_price(ticker=ticker, k=best_k)
            current_price = upbit_get_info.get_current_price(ticker=ticker)
            print("현재 시간 : " + str(now), end="")
            print(" BEST K : " + str(best_k), end="")
            print("target_price : {}".format(target_price))
            print("current_price : {}".format(current_price))
            
        if target_price < current_price:
            upbit_buy_and_sell.buy_crypto_current(ticker=ticker, fees=FEE, krw=upbit.get_balance("KRW"))
        
        time.sleep(1)
        
if __name__ == "__main__":
    print(str(datetime.datetime.now()))
    great_ticker = upbit_get_info.showBuyThings()
    great_ticker = great_ticker.index[0]
    if great_ticker != "KRW-DOGE":
        print(great_ticker)
        run(ticker=great_ticker)
