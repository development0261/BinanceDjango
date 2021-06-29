import datetime

import numpy as np
from binance.client import Client

api_key = "Bs0hCk8zsE6IteGIyXLPVBGEnYGhcBTjjWJfVMKSZFU5YSwiAMhx2rc1ICRcWkOa"
api_secret = "D8UdEhDFB61BSH09Kuqlrt2IAjGKPJ0I2Ok2JGzwenUCOHskQmRSqMdh3WWtaTvJ"

client = Client(api_key, api_secret)
exchange_info = client.get_exchange_info()

today_date = datetime.datetime.today().date()
today_date = today_date.strftime("%d %b, %Y")
one_week_ago = datetime.datetime.today().date() - datetime.timedelta(days=7)
one_week_ago = one_week_ago.strftime("%d %b, %Y")

days_25_ago = datetime.datetime.today().date() - datetime.timedelta(days=25)
days_25_ago = days_25_ago.strftime("%d %b, %Y")
from multiprocessing.pool import ThreadPool as Pool
# from multiprocessing import Pool

pool_size = 8  # your "parallelness"

# define worker function before a Pool is instantiated
def worker(item):
    try:
        if str(item).find('USDT')  != -1:
            klines = client.get_historical_klines(item, Client.KLINE_INTERVAL_1DAY, one_week_ago)
            klines1 = client.get_historical_klines(item, Client.KLINE_INTERVAL_1DAY, days_25_ago)
            seven_day_avg = 0
            twentyfive_day_avg= 0
            np_klines = np.array(klines).astype(float)
            if not np.any(np.isnan(np_klines)):
                seven_day_avg = np.mean(np_klines, axis=0)


            np_klines1 = np.array(klines1).astype(float)
            if not np.any(np.isnan(np_klines1)):
                twentyfive_day_avg = np.mean(np_klines1, axis=0)

            if seven_day_avg[4] > twentyfive_day_avg[4]:
                print(item)
                print(seven_day_avg[4] - twentyfive_day_avg[4])

    except Exception as e:
        pass

pool = Pool(pool_size)

for item in exchange_info['symbols']:
    pool.apply_async(worker, (item['symbol'],))

pool.close()
pool.join()