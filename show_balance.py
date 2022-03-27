import pyupbit
import time
import datetime
import main
import backtesting

access_key = None
secret_key = None
with open("pyupbit_key.txt") as f:
    lines = f.readlines()
    access_key = lines[0].strip()
    secret_key = lines[1].strip()
upbit = pyupbit.Upbit(access_key, secret_key)
#upbit.sell_market_order(ticker="KRW-POWR", volume=upbit.get_balance("POWR"))
print(upbit.get_balance("POWR"))
print(upbit.get_balances())
print(pyupbit.get_ohlcv("KRW-POWR"))
print(pyupbit.get_current_price("KRW-POWR"))

# while True:
#     #print(upbit.get_balance("KRW"))
#     #print(main.get_target_price("KRW-ADA"))
#     #print(pyupbit.get_current_price("KRW-ADA"))
#     print(pyupbit.get_current_price("KRW-POWR"))
#     time.sleep(0.5)

if __name__ == "__main__":
    main.showBuyThings()
            

