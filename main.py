import asyncio
import sys
from exchange_rate import ExchangeRateFetcher

async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <days> [<currency1> <currency2> ...]")
        return

    days = int(sys.argv[1])
    currencies = sys.argv[2:] if len(sys.argv) > 2 else ['EUR', 'USD']

    fetcher = ExchangeRateFetcher(days, currencies)
    rates = await fetcher.get_exchange_rates()

    for rate in rates:
        print(rate)

if __name__ == '__main__':
    asyncio.run(main())
