import os
import pandas as pd
import sqlalchemy
import asyncio
import sys
import subprocess
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
bsm = BinanceSocketManager(client)
socket = bsm.trade_socket('BTCUSDT')
engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')
loop = asyncio.get_event_loop()

def createFrame(msg):
  df = pd.DataFrame([msg])
  df = df.loc[:,['s','E','p']]
  df.columns = ['symbol','Time','Price']
  df.Price = df.Price.astype(float)
  df.Time = pd.to_datetime(df.Time, unit='ms')
  return df


async def outputbt(socket):
  while True:
    time.sleep(5)
    await socket.__aenter__()
    msg = await socket.recv()
    df = createFrame(msg)
    df.to_sql('BTCUSDT', engine, if_exists='append', index= False)
    print(df)


loop.run_until_complete(outputbt(socket))


