from datetime import datetime, date, timedelta
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

    # Params:
    # - end_date: a '%Y-%m-%d' string. Default is today.
    # - start_date: a '%Y-%m-%d' string. Default is 60 days from end_date.
    # Returned data is capped to 1000 records.
    def getPricesBetween(self, exchange, symbol,
                            start_date=None, end_date=None):
        date_format = '%Y-%m-%d'
        default_record_count = 60
        if end_date:
            end_date = datetime.strptime(end_date, date_format)
        else:
            end_date = datetime.now()
        if start_date:
            start_date = datetime.strptime(start_date, date_format)
        else:
            start_date = end_date - timedelta(days = default_record_count)
        if end_date < start_date:
            tmp = start_date
            start_date = end_date
            end_date = tmp
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        url = f'{self.domain}/stock.json?l=prices'
        url += f'&exchange={exchange}&symbol={symbol}'
        url += f'&{self.getCreds()}'
        url += f'&start_date={start_str}'
        url += f'&end_date={end_str}'
        return self.getResult(url, 'eod_list')

    def getPrices(self, exchange, symbol, lookback, page = 1): 
        url = f'{self.domain}/stock.json?l=recent_prices'
        url += f'&exchange={exchange}&symbol={symbol}'
        url += f'&{self.getCreds()}&lookback={lookback}'
        url += f'&page={page}'
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

    # Params:
    # - end_date: a '%Y-%m-%d' string. Default is today.
    # - start_date: a '%Y-%m-%d' string. Default is 60 days from end_date.
    # Returned data is capped to 1000 records.
    def getPortfolioTransactionsBetween(self, start_date=None, end_date=None,
                                        label_id=None):
        date_format = '%Y-%m-%d'
        default_record_count = 60
        if end_date:
            end_date = datetime.strptime(end_date, date_format)
        else:
            end_date = datetime.now()
        if start_date:
            start_date = datetime.strptime(start_date, date_format)
        else:
            start_date = end_date - timedelta(days = default_record_count)
        if end_date < start_date:
            tmp = start_date
            start_date = end_date
            end_date = tmp
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        url = f'{self.domain}/portfolio.json?l=portfolio_transactions_by_date'
        url += f'&{self.getCreds()}'
        url += f'&start_date={start_str}'
        url += f'&end_date={end_str}'
        url += f'&label_id={label_id}'
        
        return self.getResult(url, 'data')

    # Params
    # - open_only: True means open positions. False means closed positions.
    # - label_id: ID of portfolio to retrieve. None (default): all portfolios.
    def getPortfolio(self, label_id=None, open_only = True):
        if open_only:
            open_closed = 'current'
        else:
            open_closed = 'closed'
        url = f'{self.domain}/portfolio.json?l={open_closed}'
        url += f'&label_id={label_id}'
        url += f'&{self.getCreds()}'
        return self.getResult(url, 'data')