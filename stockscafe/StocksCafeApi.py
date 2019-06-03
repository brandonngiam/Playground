from datetime import datetime, date, timedelta
import requests
from pandas.io.json import json_normalize

class StocksCafeApi(object):
    domain = 'https://api.stocks.cafe'
    __default_lookback_days__ = 60

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

    # Given start and end date strings, return santized versions.
    # Sanitization includes
    # - Ensuring start date < end date
    # - Setting a default start_date if no value was passed.
    # - Setting end_date to today if no value was passed.
    # Params:
    # - end_date: a date string. Default is today.
    # - start_date: a '%Y-%m-%d' string.
    #               Defaults to __default_lookback_days__ days from end_date.
    # - date_format: Date string format of parameters and return values.
    # Returns:
    # - A tuple of (start_str, end_str)
    def __prepareStartEndDateStr__(self, start_date = None, end_date = None,
                                    date_format = '%Y-%m-%d'):
        if end_date:
            end_date = datetime.strptime(end_date, date_format)
        else:
            end_date = datetime.now()
        if start_date:
            start_date = datetime.strptime(start_date, date_format)
        else:
            start_date = end_date - timedelta(
                                        days = self.__default_lookback_days__)
        if end_date < start_date:
            tmp = start_date
            start_date = end_date
            end_date = tmp
        start_str = start_date.strftime(date_format)
        end_str = end_date.strftime(date_format)
        return (start_str, end_str)


    def getCreds(self):
        return 'api_user={}&api_user_key={}'.format(
                self.apiUser, self.apiUserKey)

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
        url = '{}/user.json?l=count&{}'.format(self.domain, self.getCreds())
        r = requests.get(url)
        return json_normalize(r.json())

    # Params:
    # - end_date: a '%Y-%m-%d' string. Default is today.
    # - start_date: a '%Y-%m-%d' string.
    #               Defaults to __default_lookback_days__ days from end_date.
    def getPricesBetween(self, exchange, symbol,
                            start_date = None, end_date = None):

        (start_str, end_str) = self.__prepareStartEndDateStr__(
                                        start_date, end_date)
        url = '{}/stock.json?l=prices'.format(self.domain)
        url += '&exchange={}&symbol={}'.format(exchange, symbol)
        url += '&{}'.format(self.getCreds())
        url += '&start_date={}&end_date={}'.format(start_str, end_str)
        return self.getResult(url, 'eod_list')

    def getPrices(self, exchange, symbol, lookback, page = 1): 
        url = '{}/stock.json?l=recent_prices'.format(self.domain)
        url += '&exchange={}&symbol={}'.format(exchange, symbol)
        url += '&{}&lookback={}'.format(self.getCreds(), lookback)
        url += '&page={}'.format(page)
        return self.getResult(url, 'eod_list')

    def getCollectedDividends(self, startDate, endDate):
        url = '{}/portfolio.json?l=collected_dividends'.format(self.domain)
        url += '&{}&start_date={}&end_date={}'.format(
                                        self.getCreds(), startDate, endDate)
        return self.getResult(url, 'data')

    def getPortfolioTransactions(self, page = 1):
        url = '{}/portfolio.json?l=portfolio_transactions'.format(self.domain)
        url += '&page={}&{}'.format(page, self.getCreds())
        return self.getResult(url, 'data')

    # Params:
    # - end_date: a '%Y-%m-%d' string. Default is today.
    # - start_date: a '%Y-%m-%d' string.
    #               Defaults to __default_lookback_days__ days from end_date.
    # Returned data is capped to 1000 records.
    def getPortfolioTransactionsBetween(self, start_date = None,
                                        end_date = None, label_id = None):
        (start_str, end_str) = self.__prepareStartEndDateStr__(
                                        start_date, end_date)
        url = '{}/portfolio.json?l=portfolio_transactions_by_date'.format(
                    self.domain)
        url += '&{}'.format(self.getCreds())
        url += '&start_date={}&end_date={}'.format(start_str, end_str)
        url += '&label_id={}'.format(label_id)
        
        return self.getResult(url, 'data')

    # Params
    # - open_only: True means open positions. False means closed positions.
    # - label_id: ID of portfolio to retrieve. None (default): all portfolios.
    def getPortfolio(self, label_id = None, open_only = True):
        if open_only:
            open_closed = 'current'
        else:
            open_closed = 'closed'
        url = '{}/portfolio.json?l={}'.format(self.domain, open_closed)
        url += '&label_id={}&{}'.format(label_id, self.getCreds())
        return self.getResult(url, 'data')