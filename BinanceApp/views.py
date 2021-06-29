import datetime
from binance import Client
from django.http import JsonResponse
from django.shortcuts import render
import numpy as np
from multiprocessing.pool import ThreadPool as Pool

pool_size = 8



BINANCE_API_KEY = "Bs0hCk8zsE6IteGIyXLPVBGEnYGhcBTjjWJfVMKSZFU5YSwiAMhx2rc1ICRcWkOa"
BINANCE_SECRET_KEY = "D8UdEhDFB61BSH09Kuqlrt2IAjGKPJ0I2Ok2JGzwenUCOHskQmRSqMdh3WWtaTvJ"
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
today_date = datetime.datetime.today().date()
today_date = today_date.strftime("%d %b, %Y")
one_week_ago = datetime.datetime.today().date() - datetime.timedelta(days=7)
one_week_ago = one_week_ago.strftime("%d %b, %Y")
days_25_ago = datetime.datetime.today().date() - datetime.timedelta(days=25)
days_25_ago = days_25_ago.strftime("%d %b, %Y")


crypto_list = []
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
                crypto_list.append(item)


    except Exception as e:
        pass




def index(request):

    return render(request,"index.html")

def get_coins(request):
    exchange_info = client.get_exchange_info()
    pool = Pool(pool_size)
    for item in exchange_info['symbols']:
        pool.apply_async(worker, (item['symbol'],))

    pool.close()
    pool.join()

    return JsonResponse({'msg':"Success","coins":crypto_list})

def get_coin_price(request):

    coin = request.POST['coin']

    interval = request.POST['interval']

    kinterval = ''
    if interval == "1Hour":
        kinterval = Client.KLINE_INTERVAL_1HOUR
    elif interval == "4Hours":
        kinterval = Client.KLINE_INTERVAL_4HOUR
    elif interval == "1Day":
        kinterval = Client.KLINE_INTERVAL_1DAY
    elif interval == "1Week":

        kinterval = Client.KLINE_INTERVAL_1WEEK

    klines = client.get_klines(symbol=coin, interval=kinterval)

    coin_price = []
    for i in range(len(klines)-1,len(klines)-51,-1):
        coin_data = dict()
        coin_data['TimeStamp'] = datetime.datetime.fromtimestamp(klines[i][0] / 1000.0).strftime("%b %d %Y %H:%M:%S")
        coin_data['Price'] = klines[i][1]
        coin_price.append(coin_data)



    return JsonResponse({'msg':'Success','coin_prices':coin_price})
