import upbit_get_info as info
import datetime
import pyupbit
from sys import stdout
def get_best_coin(now):
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
    
def run():
    now = datetime.datetime(2021,1,1,9,0,0,0)
    while True:
        