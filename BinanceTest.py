from binance.client import Client

api_key = "Bs0hCk8zsE6IteGIyXLPVBGEnYGhcBTjjWJfVMKSZFU5YSwiAMhx2rc1ICRcWkOa"
api_secret = "D8UdEhDFB61BSH09Kuqlrt2IAjGKPJ0I2Ok2JGzwenUCOHskQmRSqMdh3WWtaTvJ"

client = Client(api_key, api_secret)
exchange_info = client.get_exchange_info()
counter = 0
for s in exchange_info['symbols']:
    if str(s['symbol']).find('USDT') != -1:
        counter = counter +1
        print(s['symbol'])

print(counter)