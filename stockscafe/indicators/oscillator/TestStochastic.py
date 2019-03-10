from . import Stochastic
import unittest
import numpy as np
import pandas as pd
from ...utils import Comparison

class TestStochastic(unittest.TestCase):
    # http://investexcel.net/how-to-calculate-the-stochastic-oscillator/
    def testCompute(self):
        input = {
            'date': [   '15 Dec 2009', '16 Dec 2009', '17 Dec 2009', '18 Dec 2009', '21 Dec 2009',
                        '22 Dec 2009', '23 Dec 2009', '24 Dec 2009', '28 Dec 2009', '29 Dec 2009',
                        '30 Dec 2009', '31 Dec 2009',  '4 Jan 2009', '5 Jan 2009' , '6 Jan 2009' ,
                        '7 Jan 2009'],
            
            'high': [   1565.55, 1579.58, 1583.00, 1592.64, 1585.78,
                        1596.65, 1597.57, 1597.55, 1598.60, 1618.46,
                        1619.77, 1626.03, 1632.78, 1635.01, 1633.70,
                        1636.00],

            'low': [    1548.19, 1562.50, 1575.80, 1578.93, 1577.56,
                        1582.34, 1586.50, 1581.28, 1582.77, 1597.60,
                        1614.21, 1616.64, 1622.70, 1623.09, 1623.71,
                        1626.74],

            'close': [  1562.50, 1578.78, 1578.79, 1585.16, 1582.24,
                        1593.61, 1597.57, 1582.70, 1597.59, 1614.42,
                        1617.50, 1625.96, 1632.69, 1626.67, 1633.70,
                        1633.77]        
        }
        k_exp_output = [    np.nan, np.nan, np.nan, np.nan, np.nan,
                            np.nan, np.nan, np.nan, np.nan, np.nan,
                            np.nan, np.nan, np.nan, 90.39, 98.19,
                            96.29]
        d_exp_output = [    np.nan, np.nan, np.nan, np.nan, np.nan,
                            np.nan, np.nan, np.nan, np.nan, np.nan,
                            np.nan, np.nan, np.nan, np.nan, np.nan,
                            94.96]

        expected_output2 = []
        inputDf = pd.DataFrame(data = input)
        outputDf = Stochastic.compute(inputDf, 14, 3)
        outputK = outputDf['%K14']
        outputD = outputDf['%D3']
        self.assertTrue(Comparison.compareNumbers(outputK, k_exp_output, 0.01, False))
        self.assertTrue(Comparison.compareNumbers(outputD, d_exp_output, 0.01, False))

    # https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:stochastic_oscillator_fast_slow_and_full
    def testCompute2(self):
        input = {
            'date': [   '15 Dec 2009', '16 Dec 2009', '17 Dec 2009', '18 Dec 2009', '21 Dec 2009',
                        '22 Dec 2009', '23 Dec 2009', '24 Dec 2009', '28 Dec 2009', '29 Dec 2009',
                        '30 Dec 2009', '31 Dec 2009',  '4 Jan 2009', '5 Jan 2009' , '6 Jan 2009' ,
                        '7 Jan 2009' , '8 Jan 2009' , '11 Jan 2009', '12 Jan 2009', '13 Jan 2009',
                        '14 Jan 2009', '15 Jan 2009', '19 Jan 2009', '20 Jan 2009', '21 Jan 2009',
                        '22 Jan 2009', '25 Jan 2009', '26 Jan 2009', '27 Jan 2009', '28 Jan 2009'],

            'high': [   127.01, 127.62, 126.59, 127.35, 128.17,
                        128.43, 127.37, 126.42, 126.90, 126.85,
                        125.65, 125.72, 127.16, 127.72, 127.69,
                        128.22, 128.27, 128.09, 128.27, 127.74, 
                        128.77, 129.29, 130.06, 129.12, 129.29,
                        128.47, 128.09, 128.65, 129.14, 128.64],

            'low': [    125.36, 126.16, 124.93, 126.09, 126.82,
                        126.48, 126.03, 124.83, 126.39, 125.72,  
                        124.56, 124.57, 125.07, 126.86, 126.63,
                        126.80, 126.71, 126.80, 126.13, 125.92, 
                        126.99, 127.81, 128.47, 128.06, 127.61,
                        127.60, 127.00, 126.90, 127.49, 127.40],

            'close': [  np.nan, np.nan, np.nan, np.nan, np.nan,
                        np.nan, np.nan, np.nan, np.nan, np.nan,
                        np.nan, np.nan, np.nan, 127.29, 127.18,
                        128.01, 127.11, 127.73, 127.06, 127.33,
                        128.71, 127.87, 128.58, 128.60, 127.93,
                        128.11, 127.60, 127.60, 128.69, 128.27]}

        expected_output = [ np.nan, np.nan, np.nan, np.nan, np.nan,
                            np.nan, np.nan, np.nan, np.nan, np.nan,
                            np.nan, np.nan, np.nan, 70.44, 67.61, 
                            89.20, 65.81, 81.75, 64.52, 74.53, 
                            98.58, 70.10, 73.06, 73.42, 61.23, 
                            60.96, 40.39, 40.39, 66.83, 56.73]
        inputDf = pd.DataFrame(data = input)
        output = Stochastic.compute(inputDf, 14, 3)['%K14']
        self.assertTrue(Comparison.compareNumbers(output, expected_output, 0.2, False))