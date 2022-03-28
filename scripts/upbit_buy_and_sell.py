import account_keys
import upbit_get_info
import pyupbit

access_key, secret_key = account_keys.get_keys()
upbit = pyupbit.Upbit(access_key, secret_key)

def buy_crypto_current(ticker, fees, krw=None):
    '''
        ticker : 구매할 코인 종목
        krw : 구매할 원화량
        
        print buy_info
    '''
    if krw is None:
        krw = upbit.get_balance(ticker = "KRW") # get_info에서 가져오기로 변경하기
    krw_commision = krw*(1-fees)
    if krw_commision > 5000:
        print("\n#### BUY CRYPTO_CURRENT ####")
        ret = upbit.buy_market_order(ticker, krw*(1-fees))
        if ret is not None:
            print(ret)
        print("구매 코인 : {}, 구매한 원화량 : {}"
            .format(ticker, krw_commision))
    
def buy_crypto_limit(ticker, unit, fees, krw = None):
    '''
        ticker : 구매할 코인 종목
        unit : 구매할 코인량
        krw : 구매할 원화량
        
        print buy_info
    '''
    print("\n#### BUY CRYPTO_LIMIT ####")
    if krw is None:
        krw = upbit.get_balance(ticker = "KRW") # get_info에서 가져오기로 변경하기
    krw_commision = (1-fees) * krw
    real_current_price = upbit_get_info.get_current_price(ticker=ticker)
    upbit.buy_limit_order(ticker, real_current_price, unit)
    ret = upbit.buy_market_order(ticker, krw_commision)
    if ret is not None:
        print(ret)
    print("구매 코인 : {}, 구매한 코인량 : {}, 구매한 원화량 : {}"
          .format(ticker, unit, krw_commision))
    
def sell_crypto_currency(ticker, unit):
    '''
        ticker : 판매할 코인 종목
        unit : 판매할 코인 수
        
        print sell_info
    '''
    print("\n#### BUY CRYPTO_LIMIT ####")
    ret = upbit.sell_market_order(ticker=ticker, volume=unit)
    if ret is not None:
        print(ret)
    print("판매 개수 : {}".format(unit))