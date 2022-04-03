import upbit_buy_and_sell
import upbit_get_info as info
import upbit_print
import account_keys
import pyupbit
import datetime
import time

access_key, secret_key = account_keys.get_keys()
upbit = pyupbit.Upbit(access=access_key, secret=secret_key)

FEE = 0.0005


def findcoin():
    great_ticker = info.showBuyThings().index[0]
    if great_ticker != "KRW-DOGE":
        print("GREAT_TICKER : {}".format(great_ticker))
        return great_ticker

def run(ticker=None, cutline=10):
    while True:
        if ticker is None:
            ticker = findcoin()
        
        # 들어온 ticker가 내 코인인지 확인
        if info.ismycoin(ticker=ticker, upbit=upbit):
            K, target_price, current_price, avg_buy_price, market_open = info.Update(ticker=ticker, upbit=upbit)
            
            upbit_print.print_info(
                    ticker=ticker,
                    target_price=target_price,
                    current_price=current_price,
                    avg_buy_price=avg_buy_price,
                    k=K,
                    market_open=market_open)
            
            if market_open < datetime.datetime.now() < market_open + datetime.timedelta(seconds=10):
                upbit_buy_and_sell.sell_crypto_currency(ticker=ticker, unit=upbit.get_balance(ticker=ticker))
                ticker = None
            
            if avg_buy_price > current_price:
                dmg_percent = (1 - (current_price / avg_buy_price)) * 100
                if dmg_percent > cutline:
                    upbit_buy_and_sell.sell_crypto_currency(ticker=ticker, unit=upbit.get_balance(ticker=ticker))
                    ticker = None
                else:
                    print("손해 BUT IN CUTLINE!")
            # else:
                # 이익이라면

        else: # 그 코인이 없다면 살지 말지 고민하기
            K, target_price, current_price, avg_buy_price, market_open = info.Update(ticker=ticker, upbit=upbit)
            if upbit.get_balance(ticker="KRW")*(1+FEE) > 5000:
                print("gap이 가장 큰 코인을 소유하고 있지 않습니다. 구매합니다.")
                upbit_buy_and_sell.buy_crypto_current(ticker=ticker, fees=FEE)
            else: # ticker 변경
                ticker = info.get_my_coin(upbit=upbit, no_names=['KRW', 'VTHO', 'DOGE'])
                
            

if __name__ == "__main__":
    #print(str(datetime.datetime.now()))
    # run(ticker="KRW-NEAR", cutline=10)
    # run()
    run(ticker="KRW-NEAR")