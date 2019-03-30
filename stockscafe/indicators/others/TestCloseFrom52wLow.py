from . import CloseFrom52wLow as indicator
from datetime import date, timedelta
import random
import pandas as pd
import numpy as np
import unittest

class TestCloseFrom52wLow(unittest.TestCase):
    def test_compute(self):
        print("TestCloseFrom52wLow.testCompute")
        # Test parameters.
        test_window_weeks = 1
        round_decimal_places = 4
        # Test data.
        columns = ['date', 'close', 'high', 'low', '1w_low', '1w_high',
            '1w_close_percent']
        expected_results = [
            {
                "date": "13 Jun 2010", "close": 0.3079881654,
                "high": 0.4860189517, "low": 0.1680695112,
                "1w_low": np.nan, "1w_high": np.nan,
                "1w_close_percent": np.nan},
            {
                "date": "14 Jun 2010", "close": 3.45159509,
                "high": 4.8104719363, "low": 2.4267783946,
                "1w_low": np.nan, "1w_high": np.nan,
                "1w_close_percent": np.nan},
            {
                "date": "15 Jun 2010", "close": 3.73695437,
                "high": 4.1938180662, "low": 1.4049508203,
                "1w_low": np.nan, "1w_high": np.nan,
                "1w_close_percent": np.nan},
            {
                "date": "29 Jul 2010", "close": 3.8046192167,
                "high": 3.8924975796, "low": 1.9777489132,
                "1w_low": np.nan, "1w_high": np.nan,
                "1w_close_percent": np.nan},
            {
                "date": "30 Jul 2010", "close": 2.596182346,
                "high": 4.4788292482, "low": 1.0349382307,
                "1w_low": 0.1680695112, "1w_high": 4.8104719363,
                "1w_close_percent": 52.3029374129},
            {
                "date": "31 Jul 2010", "close": 9.4279977091,
                "high": 10.2236292077, "low": 6.5313745197,
                "1w_low": 1.0349382307, "1w_high": 10.2236292077,
                "1w_close_percent": 91.3411877653},
            {
                "date": "1 Aug 2010", "close": 13.7205577401,
                "high": 15.7109200017, "low": 4.9819342208,
                "1w_low": 1.0349382307, "1w_high": 15.7109200017,
                "1w_close_percent": 86.4379617482},
            {
                "date": "9 Aug 2010", "close": 11.0747856776,
                "high": 11.4115224579, "low": 1.743673471,
                "1w_low": 1.0349382307, "1w_high": 15.7109200017,
                "1w_close_percent": 68.4100566735},
            {
                "date": "10 Aug 2010", "close": 7.6184044667,
                "high": 9.2396525398, "low": 0.8529161652,
                "1w_low": 0.8529161652, "1w_high": 15.7109200017,
                "1w_close_percent": 45.5343017538},
            {
                "date": "11 Aug 2010", "close": 5.3458553592,
                "high": 6.9140403028, "low": 2.063804013,
                "1w_low": 0.8529161652, "1w_high": 15.7109200017,
                "1w_close_percent": 30.2391845064},
            {
                "date": "12 Aug 2010", "close": 12.0633803946,
                "high": 12.8140411972, "low": 9.0127575457,
                "1w_low": 0.8529161652, "1w_high": 15.7109200017,
                "1w_close_percent": 75.4506752912},
            {
                "date": "13 Aug 2010", "close": 19.477767578,
                "high": 20.9289048387, "low": 3.2510756875,
                "1w_low": 0.8529161652, "1w_high": 20.9289048387,
                "1w_close_percent": 92.7717768512}
        ]
        expected = pd.DataFrame(expected_results)[columns]
        # Split out the price data.
        prices = expected[['date', 'close', 'high', 'low']].copy()
        # Apply indicator.
        result = indicator.compute(prices, window = test_window_weeks)
        # Round down decimals in case computed results are more refined.
        expected = expected.round(round_decimal_places)
        result = result.round(round_decimal_places)
        self.assertTrue(result['date'].equals(expected['date']))
        #self.assertTrue(result.equals(expected))

        # Test with a few iterations of randomize price rows.
        iterations = 5
        for i in range(0, iterations):
            random_data = expected_results
            random.shuffle(random_data)
            # Split out the randomized price data.
            random_prices = pd.DataFrame(random_data)[[
                'date', 'close', 'high', 'low']]
            del(random_data)
            # Apply indicator.
            random_result = indicator.compute(
                random_prices, window = test_window_weeks)
            random_result = random_result.round(round_decimal_places)
            self.assertTrue(random_result.equals(expected))
