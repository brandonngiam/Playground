import requests
from pandas.io.json import json_normalize

class StocksCafe(object):
    domain = 'https://api.stocks.cafe'
    recentPricesUrl = f'{domain}/stock.json?l=recent_prices'
    apiCountUrl = f'{domain}/user.json?l=count'
    collectedDividendsUrl = f'{domain}/portfolio.json?l=collected_dividends'

    def __init__(self, api_key_file='api-key.txt', apiUser='', apiUserKey=''):
        if apiUser != '' or apiUserKey != '':
            self.apiUser = apiUser
            self.apiUserKey = apiUserKey
        else:
            f = open(api_key_file, "r") 
            self.apiUser = f.readline().rstrip() # First line shall be api_user
            self.apiUserKey = f.readline().rstrip() # Second line shall be api_user_key

    def getCreds(self):
        return f'api_user={self.apiUser}&api_user_key={self.apiUserKey}'

    def getResult(self, url, result_key): # result_key is where the data sits
        json = requests.get(url).json()
        if json['result_boolean']:
            array = json[result_key]
            return json_normalize(array)
        else:
            raise Exception(json['result'])

    def getApiCount(self):
        url = f'{self.apiCountUrl}&{self.getCreds()}'
        r = requests.get(url)
        return json_normalize(r.json())

    def getPrices(self, exchange, symbol, lookback): 
        url = f'{self.recentPricesUrl}&exchange={exchange}&symbol={symbol}&{self.getCreds()}&lookback={lookback}'
        return self.getResult(url, 'eod_list')

    def getCollectedDividends(self, startDate, endDate):
        url = f'{self.collectedDividendsUrl}&{self.getCreds()}&start_date={startDate}&end_date={endDate}'
        return self.getResult(url, 'data')
