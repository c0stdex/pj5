import aiohttp
import asyncio
from datetime import datetime, timedelta

class ExchangeRateFetcher:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    def __init__(self, days: int, currencies: list):
        self.days = min(days, 10)
        self.currencies = currencies

    async def fetch_rates(self, date: str):
        params = {'json': '', 'date': date}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None

    async def get_exchange_rates(self):
        end_date = datetime.now()
        dates = [(end_date - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(self.days)]

        results = []
        for date in dates:
            data = await self.fetch_rates(date)
            if data:
                rates = {currency: {'sale': None, 'purchase': None} for currency in self.currencies}
                for rate in data.get('exchangeRate', []):
                    if rate['currency'] in self.currencies:
                        rates[rate['currency']] = {
                            'sale': rate.get('saleRateNB'),
                            'purchase': rate.get('purchaseRateNB')
                        }
                results.append({date: rates})

        return results

async def main(days: int, currencies: list):
    fetcher = ExchangeRateFetcher(days, currencies)
    rates = await fetcher.get_exchange_rates()
    print(rates)

if __name__ == '__main__':
    import sys
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    currencies = sys.argv[2:] if len(sys.argv) > 2 else ['EUR', 'USD']
    asyncio.run(main(days, currencies))
