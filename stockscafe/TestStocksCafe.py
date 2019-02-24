import unittest
from .StocksCafe import StocksCafe

class TestStocksCafe(unittest.TestCase):
    def testGetPrices(self):
        print("TestStocksCafe.testGetPrices")
        sc = StocksCafe()
        df = sc.getPrices('SGX', 'D05', 5)
        self.assertTrue('change' in df.columns)
        self.assertTrue('high' in df.columns)
        self.assertTrue('low' in df.columns)
        self.assertTrue('open' in df.columns)
        self.assertTrue('close' in df.columns)
        self.assertTrue('date' in df.columns)
        self.assertTrue('volume' in df.columns)
        self.assertTrue(len(df.index) == 5)

    def testApiCount(self):
        print("TestStocksCafe.testApiCount")
        sc = StocksCafe()
        df = sc.getApiCount()
        self.assertTrue('count' in df.columns)
