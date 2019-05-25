import unittest
from datetime import datetime
import pandas as pd
from .StocksCafeApi import StocksCafeApi

class TestStocksCafeApi(unittest.TestCase):
    def testGetPrices(self):
        print("TestStocksCafe.testGetPrices")
        sc = StocksCafeApi()
        df = sc.getPrices('SGX', 'D05', 5)['eod_list']
        self.assertTrue('change' in df.columns)
        self.assertTrue('high' in df.columns)
        self.assertTrue('low' in df.columns)
        self.assertTrue('open' in df.columns)
        self.assertTrue('close' in df.columns)
        self.assertTrue('date' in df.columns)
        self.assertTrue('volume' in df.columns)
        self.assertTrue(len(df.index) == 5)

    def testUsageCount(self):
        print("TestStocksCafe.testUsageCount")
        sc = StocksCafeApi()
        df = sc.getUsageCount()
        self.assertTrue('count' in df.columns)

    def testGetCollectedDividends(self):
        print("TestStocksCafe.testGetCollectedDividends")
        expected_columns = [
            'base_curr', 'base_curr_div_amt', 'base_curr_div_amt_after_tax',
            'currency', 'div_amt', 'div_amt_after_tax', 'ex_date', 'exchange',
            'pay_date', 'shares', 'symbol']
        sc = StocksCafeApi()
        df = sc.getCollectedDividends('2019-05-01', '2019-05-24')['data']
        for expected_column in expected_columns:
            self.assertTrue(expected_column in df.columns)

    def testgetPortfolioTransactions(self):
        print("TestStocksCafe.testGetPortfolioTransactions")
        expected_columns = ['add_to_cash', 'currency', 'date', 'exchange',
            'fees', 'fees_percent', 'fees_percent_string', 'fees_string',
            'label_id', 'name', 'notes', 'price', 'price_string',
            'scrip_dividend', 'shares', 'shares_string', 'symbol',
            'total_value', 'total_value_string', 'transaction_id', 'type']
        sc = StocksCafeApi()
        df = sc.getPortfolioTransactions()['data']
        for expected_column in expected_columns:
            self.assertTrue(expected_column in df.columns)

    def testGetPricesBetween(self):
        print("TestStocksCafe.testGetPricesBetween")
        expected_columns = ['change', 'change_percent', 'close', 'currency',
            'date', 'high', 'low', 'open', 'volume']
        exchange = 'SGX'
        symbol = 'U11'
        start_date  = '2019-05-02'
        end_date  = '2019-05-24'
        sc = StocksCafeApi()
        df = sc.getPricesBetween(exchange, symbol,
                                    start_date=start_date, end_date=end_date
                                )['eod_list']
        df['date_obj'] = pd.to_datetime(df['date'], format='%d %b %Y')
        assert(start_date == df['date_obj'].min().strftime('%Y-%m-%d'))
        assert(end_date == df['date_obj'].max().strftime('%Y-%m-%d'))
        for expected_column in expected_columns:
            self.assertTrue(expected_column in df.columns)

    def testGetPortfolioTransactionsBetween(self):
        print("TestStocksCafe.testGetPortfolioTransactionsBetween")
        expected_columns = ['add_to_cash', 'currency', 'date', 'exchange',
            'fees', 'fees_percent', 'fees_percent_string', 'fees_string',
            'label_id', 'name', 'notes', 'price', 'price_string',
            'scrip_dividend', 'shares', 'shares_string', 'symbol',
            'total_value', 'total_value_string', 'transaction_id',
            'type', 'date_obj']
        start_date  = '2018-01-01'
        end_date  = '2019-01-01'
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        sc = StocksCafeApi()
        df = sc.getPortfolioTransactionsBetween(start_date = start_date,
                                    end_date = end_date, label_id=None)['data']
        df['date_obj'] = pd.to_datetime(df['date'], format='%d %b %Y')
        assert(start_date_obj <= df['date_obj'].min())
        assert(end_date_obj >= df['date_obj'].max())
        for expected_column in expected_columns:
            self.assertTrue(expected_column in df.columns)

    def testGetPortfolio(self):
        print("TestStocksCafe.testGetPortfolio")
        expected_columns = ['average_price', 'average_price_string', 'close',
            'currency', 'current_pl_with_dividends',
            'current_pl_with_dividends_percent',
            'current_pl_with_dividends_percent_string',
            'current_pl_with_dividends_string', 'day_change',
            'day_change_percent', 'day_change_percent_string',
            'day_change_string', 'exchange', 'name', 'shares', 'shares_string',
            'symbol']
        sc = StocksCafeApi()
        df = sc.getPortfolio(label_id=None, open_only = True)['data']
        for expected_column in expected_columns:
            self.assertTrue(expected_column in df.columns)
