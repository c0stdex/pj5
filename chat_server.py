import asyncio
import websockets
import json
from exchange_rate import ExchangeRateFetcher
from datetime import datetime
from aiofile import AIOFile, Writer

clients = set()

async def log_exchange_command(command):
    async with AIOFile("exchange_log.txt", 'a') as afp:
        writer = Writer(afp)
        await writer(f"{datetime.now()}: {command}\n")

async def send_exchange_rate(websocket, days, currencies):
    fetcher = ExchangeRateFetcher(days, currencies)
    rates = await fetcher.get_exchange_rates()
    await websocket.send(json.dumps(rates))

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            command = message.strip().split()
            if command[0] == "exchange":
                days = int(command[1]) if len(command) > 1 else 1
                currencies = command[2:] if len(command) > 2 else ['EUR', 'USD']
                await log_exchange_command(message)
                await send_exchange_rate(websocket, days, currencies)
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()
if __name__ == '__main__':
    asyncio.run(main())
