import datetime

import numpy as np
from binance import Client
import pandas

BINANCE_API_KEY = "Bs0hCk8zsE6IteGIyXLPVBGEnYGhcBTjjWJfVMKSZFU5YSwiAMhx2rc1ICRcWkOa"
BINANCE_SECRET_KEY = "D8UdEhDFB61BSH09Kuqlrt2IAjGKPJ0I2Ok2JGzwenUCOHskQmRSqMdh3WWtaTvJ"


client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
today_date = datetime.datetime.today().date()
today_date = today_date.strftime("%d %b, %Y")
one_week_ago = datetime.datetime.today().date() - datetime.timedelta(days=7)
one_week_ago = one_week_ago.strftime("%d %b, %Y")
days_25_ago = datetime.datetime.today().date() - datetime.timedelta(days=25)
days_25_ago = days_25_ago.strftime("%d %b, %Y")
klines = client.get_historical_klines("DOGEUSDT", Client.KLINE_INTERVAL_4HOUR, one_week_ago,today_date)
klines1 = client.get_historical_klines("DOGEUSDT", Client.KLINE_INTERVAL_4HOUR, days_25_ago)
seven_day_avg = 0
twentyfive_day_avg = 0

daily_lines = []
for line in klines:
    daily_lines.append(float(line[4]))
df = pandas.DataFrame({"Data":daily_lines})
print(df.Data.rolling(window=25).mean().iloc[-1])

