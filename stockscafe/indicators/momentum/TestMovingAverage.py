import stockscafe.indicators.momentum.MovingAverage as MA
import stockscafe.utils.Ordering as Ordering
import pandas as pd
import unittest

class TestMovingAverage(unittest.TestCase):
    def testCompute(self):
        print("TestMovingAverage.testCompute")
        input = {
            'date': [   '15 Dec 2009', '16 Dec 2009', '17 Dec 2009', '18 Dec 2009', '21 Dec 2009',
                        '22 Dec 2009', '23 Dec 2009', '24 Dec 2009', '28 Dec 2009', '29 Dec 2009',
                        '30 Dec 2009', '31 Dec 2009',  '4 Jan 2009', '5 Jan 2009' , '6 Jan 2009'],
            'close': [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            }
        output = [None, None, None, None, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] 
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
        output = [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, None, None, None, None]
        inputDf = pd.DataFrame(data = input)
        outputDf = pd.DataFrame(data = input)
        outputDf['sma5'] = output
        self.assertTrue(MA.compute(inputDf, 5).equals(Ordering.reverse(outputDf)))

