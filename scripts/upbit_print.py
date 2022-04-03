import datetime
import pyupbit
import upbit_get_info
import account_keys

access_key, secret_key = account_keys.get_keys()
upbit = pyupbit.Upbit(access_key, secret_key)

def print_info(ticker, target_price, current_price, avg_buy_price, k, market_open):
    '''
        ticker : 거래하는 코인 종목
        target/current price
        avg_buy_price : 평균 매수가
        k : best_k
        market_open : 마켓 오픈 시간

        print infos
    '''
    now = datetime.datetime.now()
    
    print("market_open : " + str(market_open))
    print("TICKER : " + str(ticker))
    print("현재 시간 : "  + str(now))
    print("BEST K : " + str(k))
    print("target price : " + str(target_price))
    print("current price : " + str(current_price))
    print("현재 KRW : " + str(upbit.get_balance("KRW")))
    print("현재 ticker : " + str(upbit.get_balance(ticker)))
    print("현재 ticker 구매 평단가 : {}".format(avg_buy_price))
    
    dmg_percent = (1-(current_price / avg_buy_price))*100
    if avg_buy_price is not None and avg_buy_price > current_price:
        print("현재 {} ({}%) 손실!".format(
              abs(avg_buy_price-current_price) * upbit.get_balance(ticker),
              dmg_percent)
            )
    else:
        print("현재 {} ({}%) 이익!".format(
              abs(avg_buy_price-current_price) * upbit.get_balance(ticker),
              ((current_price / avg_buy_price)-1)*100)
            )
    print("========================================",end='\r',flush=True)
    print("\n")
