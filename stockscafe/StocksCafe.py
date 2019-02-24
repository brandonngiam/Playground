import requests
from pandas.io.json import json_normalize

class StocksCafe(object):
    domain = 'https://api.stocks.cafe'
    recentPricesUrl = f'{domain}/stock.json?l=recent_prices'
    apiCountUrl = f'{domain}/user.json?l=count'

    def __init__(self, api_key_file='api.key'):
        f = open(api_key_file, "r") 
        self.apiUser = f.readline().rstrip() # First line shall be api_user
        self.apiUserKey = f.readline().rstrip() # Second line shall be api_user_key

    def getCreds(self):
        return f'api_user={self.apiUser}&api_user_key={self.apiUserKey}'

    def getApiCount(self):
        url = f'{self.apiCountUrl}&{self.getCreds()}'
        r = requests.get(url)
        return json_normalize(r.json())

    def getPrices(self, exchange, symbol, lookback): 
        url = f'{self.recentPricesUrl}&exchange={exchange}&symbol={symbol}&{self.getCreds()}&lookback={lookback}'
        r = requests.get(url)
        array = r.json()['eod_list']
        return json_normalize(array)