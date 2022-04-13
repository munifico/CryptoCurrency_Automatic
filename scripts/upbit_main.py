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


def findcoin(no_names=None):
    coin_list = info.showBuyThings()
    great_gap = 100
    target_ticker = None
    for g in range(len(coin_list)):
        g_gap =  coin_list['gap_ratio'][g]
        if g_gap > 0:
            if great_gap > g_gap:
                great_gap = g_gap

    for coin in range(len(coin_list)):
        if coin_list['gap_ratio'][coin] == great_gap:
            target_ticker = coin_list.index[coin]

    if target_ticker is None:
        return None

    K, target_price, current_price, avg_buy_price, market_open = info.Update(ticker=target_ticker, upbit=upbit)
    if target_price < current_price:
        if target_ticker not in no_names:
            great_ticker = target_ticker
            print("GREAT_TICKER : {}".format(great_ticker))
            print(great_ticker)
            return great_ticker
    else:
        return None


def run(ticker=None, cutline=5):
    while True:
        if ticker is None:
            ticker = findcoin(no_names=['KRW', 'VTHO', 'DOGE'])
            if ticker is None:
                my_ticker = info.get_my_coin(upbit=upbit, no_names=['KRW', 'VTHO', 'DOGE'])
                if my_ticker is None:
                    print("조건에 맞는 코인이 없습니다. 다시 검색합니다.")
                    continue
                else:
                    print("내 ticker {}를 현재 ticker로 정의합니다".format(my_ticker))
                    ticker = my_ticker
        
        # 들어온 ticker가 내 코인인지 확인
        if info.ismycoin(ticker=ticker, upbit=upbit):
            K, target_price, current_price, avg_buy_price, market_open = info.Update(ticker=ticker, upbit=upbit)

            if avg_buy_price is None: # 예외처리 : 중간에 사용자가 판매했을 경우
                ticker = None

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
            else:
                # 이익이라면
                profit_percent = ((current_price / avg_buy_price)-1)*100
                if profit_percent > 10:
                    upbit_buy_and_sell.sell_crypto_currency(ticker=ticker, unit=upbit.get_balance(ticker=ticker))
                    ticker = None

        else: # 그 코인이 없다면 살지 말지 고민하기 # 없으면 1. 가지고 있는게 아예 없어서 사야하거나 2. 가지고 있는게 있어서 그걸로 계속 할지
            my_ticker = info.get_my_coin(upbit=upbit, no_names=['KRW', 'VTHO', 'DOGE'])
            if my_ticker is None:
                if upbit.get_balance(ticker="KRW") * (1 + FEE) > 5000:
                    print("gap이 가장 큰 코인을 소유하고 있지 않습니다. 구매합니다.")
                    upbit_buy_and_sell.buy_crypto_current(ticker=ticker, fees=FEE)
            else:
                ticker = my_ticker
                
            

if __name__ == "__main__":
    #print(str(datetime.datetime.now()))
    # run(ticker="KRW-NEAR", cutline=10)
    # run()
    run()