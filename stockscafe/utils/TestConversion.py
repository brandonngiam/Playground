import unittest
import pandas as pd
from ..utils import Conversion
import datetime 

class TestConversion(unittest.TestCase):
    def testString2Date(self):
        print("TestConversion.testString2Date")
        dateObjectA = Conversion.string2DateTime('22 Feb 2019')
        self.assertEqual(datetime.datetime(2019, 2, 22), dateObjectA)
        dateObjectB = Conversion.string2DateTime('28 Jan 2019')
        self.assertTrue(datetime.datetime(2019, 1, 28) == dateObjectB)
        self.assertTrue(dateObjectA > dateObjectB)

    def testShiftTimeFrame(self):
        print("TestConversion.testShiftTimeFrame")
        input = {
            'high': [   25.07, 25.00, 25.30, 25.33, 25.29, 24.99, 24.97, 24.90, 24.41, 24.44, 
                        24.42, 24.46, 24.26, 24.13, 24.23, 24.25, 24.27, 24.40, 24.42], 
            'low': [    24.7 , 24.7 , 25.05, 25.1 , 24.89, 24.63, 24.78, 24.53, 24.28, 24.01, 
                        24.13, 24.16, 24.08, 23.9 , 23.86, 23.94, 24.03, 24.2 , 24.22], 
            'open': [   24.7 , 24.81, 25.23, 25.22, 25.  , 24.88, 24.78, 24.58, 24.39, 24.01, 
                        24.2 , 24.25, 24.12, 24.  , 24.2 , 24.25, 24.21, 24.27, 24.25], 
            'close': [  25.01, 24.81, 25.08, 25.1 , 25.2 , 24.79, 24.97, 24.9 , 24.34, 24.36, 
                        24.3 , 24.33, 24.18, 24.07, 23.92, 23.94, 24.22, 24.22, 24.22], 
            'volume': [ '4,219,570', '5,993,300', '3,509,000', '3,293,078', '5,147,100',
                        '4,885,800', '4,105,200', '5,086,200', '2,678,500', '3,230,000',
                        '2,766,386', '3,196,900', '1,911,800', '2,744,500', '5,572,800',
                        '4,043,700', '3,245,200', '2,492,300', '2,708,200'],
            'date': [   '22 Feb 2019', '21 Feb 2019', '20 Feb 2019', '19 Feb 2019', '18 Feb 2019', 
                        '15 Feb 2019', '14 Feb 2019', '13 Feb 2019', '12 Feb 2019', '11 Feb 2019', 
                        '8 Feb 2019', '7 Feb 2019', '4 Feb 2019', '1 Feb 2019', '31 Jan 2019', 
                        '30 Jan 2019', '29 Jan 2019', '28 Jan 2019', '25 Jan 2019']
            }
        expected_output = {
            'high':     [25.33, 24.99, 24.46], 
            'low':      [24.7 , 24.01, 23.86], 
            'open':     [25.0 , 24.01,  24.2], 
            'close':    [25.01, 24.79,  24.3], 
            'volume':   [22162048, 19985700, 16192386],
            'date':     ['22 Feb 2019', '15 Feb 2019', '8 Feb 2019']
        }
        df = pd.DataFrame(data = input)
        expected_output_df = pd.DataFrame(data = expected_output)
        self.assertTrue(Conversion.shiftTimeFrame(df, 5).equals(expected_output_df))

