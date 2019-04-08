import requests
from pandas.io.json import json_normalize

class StocksCafeApi(object):
    domain = 'https://api.stocks.cafe'

    def __init__(self, api_key_file='api-key.txt', apiUser='', apiUserKey=''):
        if apiUser != '' or apiUserKey != '':
            self.apiUser = apiUser
            self.apiUserKey = apiUserKey
        else:
            f = open(api_key_file, "r") 
            # First line shall be api_user
            self.apiUser = f.readline().rstrip()
            # Second line shall be api_user_key
            self.apiUserKey = f.readline().rstrip()

    def getCreds(self):
        return f'api_user={self.apiUser}&api_user_key={self.apiUserKey}'

    # result_key is where the main bulk of data sits.
    # E.g. for prices, result_key == 'eod_list'
    def getResult(self, url, result_key):
        json = requests.get(url).json()
        if json['result_boolean']:
            array = json[result_key]
            # Convert result_key to dataframe
            json[result_key] = json_normalize(array)
            return json
        else:
            raise Exception(json['result'])

    def getUsageCount(self):
        url = f'{self.domain}/user.json?l=count&{self.getCreds()}'
        r = requests.get(url)
        return json_normalize(r.json())

    def getPrices(self, exchange, symbol, lookback, page = 1): 
        url = f'{self.domain}/stock.json?l=recent_prices'
        url += f'&exchange={exchange}&symbol={symbol}'
        url += f'&{self.getCreds()}&lookback={lookback}'
        return self.getResult(url, 'eod_list')

    def getCollectedDividends(self, startDate, endDate):
        url = f'{self.domain}/portfolio.json?l=collected_dividends'
        url += f'&{self.getCreds()}&start_date={startDate}&end_date={endDate}'
        return self.getResult(url, 'data')

    def getPortfolioTransactions(self, page = 1):
        url = f'{self.domain}/portfolio.json?l=portfolio_transactions'
        url += f'&page={page}'
        url += f'&{self.getCreds()}'
        return self.getResult(url, 'data')