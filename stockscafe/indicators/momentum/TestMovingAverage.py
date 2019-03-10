from . import MovingAverage as MA
from ...utils import Ordering
from ...utils import Comparison
import pandas as pd
import numpy as np
import unittest

class TestMovingAverage(unittest.TestCase):
    def testComputeExponential(self):
        print("TestMovingAverage.testComputeExponential")
        input = {
            'date': [   '15 Dec 2009', '16 Dec 2009', '17 Dec 2009', '18 Dec 2009', '21 Dec 2009',
                        '22 Dec 2009', '23 Dec 2009', '24 Dec 2009', '28 Dec 2009', '29 Dec 2009',
                        '30 Dec 2009', '31 Dec 2009', '04 Jan 2009', '05 Jan 2009', '06 Jan 2009',
                        '07 Jan 2009', '08 Jan 2009', '09 Jan 2009', '10 Jan 2009' , '11 Jan 2009',
                        '12 Jan 2009', '13 Jan 2009', '14 Jan 2009', '15 Jan 2009' , '16 Jan 2009',
                        '17 Jan 2009', '18 Jan 2009', '19 Jan 2009', '20 Jan 2009' , '21 Jan 2009'],
            'close': [  22.27, 22.19, 22.08, 22.17, 22.18, 
                        22.13, 22.23, 22.43, 22.24, 22.29, 
                        22.15, 22.39, 22.38, 22.61, 23.36,
                        24.05, 23.75, 23.83, 23.95, 23.63,
                        23.82, 23.87, 23.65, 23.19, 23.10,
                        23.33, 22.68, 23.10, 22.40, 22.17]
            }
        expected_sma_output = [np.nan, np.nan, np.nan, np.nan, np.nan,
                        np.nan, np.nan, np.nan, np.nan, 22.221,
                        22.209, 22.229, 22.259, 22.303, 22.421,
                        22.613, 22.765, 22.905, 23.076, 23.21,
                        23.377, 23.525, 23.652, 23.71, 23.684,
                        23.612, 23.505, 23.432, 23.277, 23.131]
        expected_ema_output = [np.nan, np.nan, np.nan, np.nan, np.nan,
                        np.nan, np.nan, np.nan, np.nan, np.nan,
                        np.nan, np.nan, np.nan, np.nan, np.nan,
                        22.80, 22.97, 23.13, 23.28, 23.34,
                        23.43, 23.51, 23.54, 23.47, 23.40,
                        23.39, 23.26, 23.23, 23.08, 22.92]
        inputDf = pd.DataFrame(data = input)
        sma_output = MA.compute(inputDf, 10)['sma10']
        ema_output = MA.computeExponential(inputDf, 10)['ema10']
        self.assertTrue(Comparison.compareNumbers(sma_output, expected_sma_output, 0.01))
        self.assertTrue(Comparison.compareNumbers(ema_output, expected_ema_output, 0.01))
        
    def testCompute(self):
        print("TestMovingAverage.testCompute")
        input = {
            'date': [   '15 Dec 2009', '16 Dec 2009', '17 Dec 2009', '18 Dec 2009', '21 Dec 2009',
                        '22 Dec 2009', '23 Dec 2009', '24 Dec 2009', '28 Dec 2009', '29 Dec 2009',
                        '30 Dec 2009', '31 Dec 2009',  '4 Jan 2009', '5 Jan 2009' , '6 Jan 2009'],
            'close': [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            }
        output = [np.nan, np.nan, np.nan, np.nan, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] 
        inputDf = pd.DataFrame(data = input)
        outputDf = pd.DataFrame(data = input)
        outputDf['sma5'] = output
        self.assertTrue(MA.compute(inputDf, 5).equals(outputDf))

        input = {
            # Reversed for testing
            'date': [
                '13 Jan 2009', '12 Jan 2009', '11 Jan 2009', '8 Jan 2009', '7 Jan 2009', 
                '6 Jan 2009', '5 Jan 2009', '4 Jan 2009', '31 Dec 2009', '30 Dec 2009', 
                '29 Dec 2009', '28 Dec 2009', '24 Dec 2009', '23 Dec 2009', '22 Dec 2009', 
            ],
            'close': [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        }
        output = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, np.nan, np.nan, np.nan, np.nan]
        inputDf = pd.DataFrame(data = input)
        outputDf = pd.DataFrame(data = input)
        outputDf['sma5'] = output
        self.assertTrue(MA.compute(inputDf, 5).equals(Ordering.reverse(outputDf)))

