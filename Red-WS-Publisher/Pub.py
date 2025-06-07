import asyncio
import redis
import json
import time
import os
from alpaca.data.live import StockDataStream

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
STOCK_FILE = "/config/stocks.json"

r = redis.Redis(host=REDIS_HOST, port=6379)

def load_symbols():
    with open(STOCK_FILE, 'r') as f:
        return json.load(f)["stocks"]

symbols = load_symbols()

stream = StockDataStream(os.getenv("ALPACA_KEY"), os.getenv("ALPACA_SECRET"))

@stream.on_stock_data
async def on_data(data):
    message = json.dumps(data._raw)
    r.publish("stock_prices", message)
    print(f"Published: {message}")

async def main():
    for symbol in symbols:
        await stream.subscribe_quotes(symbol)
    while True:
        await asyncio.sleep(60)  # idle loop

if __name__ == "__main__":
    asyncio.run(main())
