import sqlalchemy
import pandas as pd
import sys
import subprocess
import os
import asyncio
import time

try:
    from binance.client import Client
    from binance import BinanceSocketManager
except ImportError as e:
  package = "python-binance"
  subprocess.check_call([sys.executable, "-m", "pip", "install", package])
  from binance.client import Client
  from binance import BinanceSocketManager

api_key = os.environ['api_key']
api_secret = os.environ['api_secret']
client = Client(api_key, api_secret)
engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')
loop = asyncio.get_event_loop()
df = pd.read_sql('BTCUSDT',engine)


async def strategy(entry, lookback, qty, open_position=False):
  while True:
    time.sleep(5)
    df = pd.read_sql('BTCUSDT')
    loopbackperiod = df.iloc[-lookback:]
    cumret = (loopbackperiod.Price.pct_change()+1).cumprod() - 1
    if not open_position:
      if cumret[cumret.last_valid_index()] > entry:
        #order = client.create_order(symbol='BTCUSDT',side='BUY',type='MARKET',quantity=qty)
        #print(order)
        open_position = True
        break

  if open_position:
    while True:
      df = pd.read_sql('BTCUSDT',engine)
      #sincebuy = df.loc[df.Time > pd.to_datetime(order['transactTime'],unit='ms')]
      #if len(sincebuy) > 1:
        #sincebuyret = (sincebuy.Price.pct_change() +1).cumprod() - 1
        #last_entry = sincebuyret[sincebuyret.last_valid_index()]
        #if last_entry > 0.0015 or last_entry < -0.0015:
          #order = client.create_order(symbol='BTCUSDT',side='SELL',type='MARKET',quantity=qty)
          #print(order)
          #break

    
