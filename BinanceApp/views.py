import datetime

from binance import Client
from dateparser.data.date_translation_data import ms
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

BINANCE_API_KEY = "Bs0hCk8zsE6IteGIyXLPVBGEnYGhcBTjjWJfVMKSZFU5YSwiAMhx2rc1ICRcWkOa"
BINANCE_SECRET_KEY = "D8UdEhDFB61BSH09Kuqlrt2IAjGKPJ0I2Ok2JGzwenUCOHskQmRSqMdh3WWtaTvJ"
client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)

def index(request):

    exchange_info = client.get_exchange_info()
    counter = 0
    crypto_list = []
    for s in exchange_info['symbols']:
        if str(s['symbol']).find('USDT') != -1:
            counter = counter + 1
            crypto_list.append(s['symbol'])



    return render(request,"index.html",{'crypto_coins':crypto_list,'counter':len(crypto_list)})

def get_coin_price(request):

    coin = request.POST['coin']
    interval = request.POST['interval']
    print(interval)
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
    for i in range(len(klines)-1,len(klines)-50,-1):
        coin_data = dict()
        coin_data['TimeStamp'] = datetime.datetime.fromtimestamp(klines[i][0] / 1000.0).strftime("%b %d %Y %H:%M:%S")
        coin_data['Price'] = klines[i][1]
        coin_price.append(coin_data)


    return JsonResponse({'msg':'Success','coin_prices':coin_price})
