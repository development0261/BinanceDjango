import datetime
from binance import Client
from django.http import JsonResponse
from django.shortcuts import render
import numpy as np
import pandas
from multiprocessing.pool import ThreadPool as Pool
import time
pool_size = 20



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

                if kinterval == Client.KLINE_INTERVAL_1WEEK:
                    print("WEEK")
                    klines = client.get_klines(symbol=item,interval= kinterval)
                    klines1 = client.get_klines(symbol=item,interval= kinterval)
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

                    # print(twentyfive_day_avg0, twentyfive_day_avg)
                    # print(seven_day_avg0, seven_day_avg)

                    if seven_day_avg > twentyfive_day_avg and seven_day_avg0 < twentyfive_day_avg0:
                        crypto_list.append({
                            'Coin': item,
                            'DMA_7': seven_day_avg,
                            'DMA_25': twentyfive_day_avg
                        })
                else:
                    klines = client.get_historical_klines(item, kinterval, one_week_ago)
                    klines1 = client.get_historical_klines(item, kinterval, days_25_ago)
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

                    # print(twentyfive_day_avg0, twentyfive_day_avg)
                    # print(seven_day_avg0, seven_day_avg)

                    if seven_day_avg > twentyfive_day_avg and seven_day_avg0 < twentyfive_day_avg0:
                        crypto_list.append({
                            'Coin': item,
                            'DMA_7': seven_day_avg,
                            'DMA_25': twentyfive_day_avg
                        })

    except Exception as e:
        pass

def index(request):
    return render(request,"index.html")



def get_coin_price(request):
    global crypto_list
    crypto_list = []
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
    symbols_fetched = client.get_all_tickers()

    pool = Pool(pool_size)
    symbols = []
    for item in symbols_fetched[:900]:
        if str(item['symbol'])[-4:] == "USDT":
            symbols.append(item['symbol'])
    for item in symbols:
        pool.apply_async(worker, (item,kinterval))
    pool.close()
    pool.join()
    coin_price = []
    try:

        for i in range(0, len(crypto_list)):
            coin_data = dict()
            coin_data['Coin'] = crypto_list[i]['Coin']
            coin_data['DMA_7'] = crypto_list[i]['DMA_7']
            coin_data['DMA_25'] = crypto_list[i]['DMA_25']
            coin_price.append(coin_data)
    except:
        pass

    return JsonResponse({'msg':'Success','coin_prices':coin_price})


def load_more(request,num_posts):
    global crypto_list


    lower =num_posts
    upper = lower + 12

    posts = []
    try:
        for i in range(lower, upper):
            coin_data = dict()
            coin_data['Coin'] = crypto_list[i]['Coin']
            coin_data['DMA_7'] = crypto_list[i]['DMA_7']
            coin_data['DMA_25'] = crypto_list[i]['DMA_25']

            posts.append(coin_data)
    except:
        pass

    posts_size = len(klines)
    max_size = True if upper >= posts_size else False
    return JsonResponse({'data': posts, 'max': max_size}, safe=False)

def load_more_view(request):
    return render(request,"LoadMore.html")

