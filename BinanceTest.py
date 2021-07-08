import datetime
from binance import Client
from django.http import JsonResponse
from django.shortcuts import render
import numpy as np
import pandas
from multiprocessing.pool import ThreadPool as Pool
import time
pool_size = 10



BINANCE_API_KEY = "Bs0hCk8zsE6IteGIyXLPVBGEnYGhcBTjjWJfVMKSZFU5YSwiAMhx2rc1ICRcWkOa"
BINANCE_SECRET_KEY = "D8UdEhDFB61BSH09Kuqlrt2IAjGKPJ0I2Ok2JGzwenUCOHskQmRSqMdh3WWtaTvJ"
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
today_date = datetime.datetime.today().date()
today_date = today_date.strftime("%d %b, %Y")
one_week_ago = datetime.datetime.today().date() - datetime.timedelta(days=7)
one_week_ago = one_week_ago.strftime("%d %b, %Y")
days_25_ago = datetime.datetime.today().date() - datetime.timedelta(days=25)
days_25_ago = days_25_ago.strftime("%d %b, %Y")

klines = []
crypto_list = []
def worker(item,kinterval):

    try:
        global crypto_list
        if str(item).find('USDT')  != -1:

                klines =  client.get_klines(symbol=item,interval= kinterval)
                klines1 =  client.get_klines(symbol=item, interval = kinterval)
                print(klines)
                print(klines1)
                seven_day_avg = 0
                twentyfive_day_avg = 0
                daily_lines = []
                for line in klines:
                    daily_lines.append(float(line[4]))
                df = pandas.DataFrame({"Data": daily_lines})
                seven_day_avg = df.Data.rolling(window=7).mean().iloc[-1]
                seven_day_avg0 = df.Data.rolling(window=7).mean().iloc[-2]

                daily_lines1 = []
                for line in klines1:
                    daily_lines1.append(float(line[4]))
                df = pandas.DataFrame({"Data": daily_lines1})

                twentyfive_day_avg = df.Data.rolling(window=25).mean().iloc[-1]
                twentyfive_day_avg0 = df.Data.rolling(window=25).mean().iloc[-2]

                print(twentyfive_day_avg0,twentyfive_day_avg)
                print(seven_day_avg0,seven_day_avg)



    except Exception as e:
        pass

def get_coin_price():
    global crypto_list
    crypto_list = []
    interval = '1Week'
    kinterval = ''
    if interval == "1Hour":
        kinterval = Client.KLINE_INTERVAL_1HOUR
    elif interval == "4Hours":
        kinterval = Client.KLINE_INTERVAL_4HOUR
    elif interval == "1Day":
        kinterval = Client.KLINE_INTERVAL_1DAY
    elif interval == "1Week":
        kinterval = Client.KLINE_INTERVAL_1WEEK
    symbols_fetched = client.get_all_tickers()

    pool = Pool(pool_size)
    symbols = []
    worker('ADAUSDT',kinterval)

get_coin_price()