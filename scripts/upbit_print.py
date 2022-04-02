import datetime
import pyupbit
import upbit_get_info
import account_keys

access_key, secret_key = account_keys.get_keys()
upbit = pyupbit.Upbit(access_key, secret_key)

def print_info(ticker, df, k, market_open):
    '''
        ticker : 거래하는 코인 종목
        df : 매매 코인의 ohlcv
        k : best_k
        market_open : 마켓 오픈 시간

        print infos
    '''
    now = datetime.datetime.now()
    target_price = upbit_get_info.get_target_price(ticker=ticker, k = k)
    current_price = pyupbit.get_current_price(ticker)
    print("market_open : " + str(market_open))
    print("TICKER : " + str(ticker))
    print("현재 시간 : "  + str(now))
    print("BEST K : " + str(k))
    print("target price : " + str(target_price))
    print("current price : " + str(current_price))
    print("현재 KRW : " + str(upbit.get_balance("KRW")))
    print("현재 ticker : " + str(upbit.get_balance(ticker)))
