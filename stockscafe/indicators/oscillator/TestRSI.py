from . import RSI
from ...utils import Ordering
import pandas as pd
import unittest

class TestRSI(unittest.TestCase):

    # https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
    def testCompute(self):
        print("TestRSI.testCompute")
        input = {
            'date': [   '15 Dec 2009', '16 Dec 2009', '17 Dec 2009', '18 Dec 2009', '21 Dec 2009',
                        '22 Dec 2009', '23 Dec 2009', '24 Dec 2009', '28 Dec 2009', '29 Dec 2009',
                        '30 Dec 2009', '31 Dec 2009',  '4 Jan 2009', '5 Jan 2009' , '6 Jan 2009' ,
                        '7 Jan 2009' , '8 Jan 2009' , '11 Jan 2009', '12 Jan 2009', '13 Jan 2009',
                        '14 Jan 2009', '15 Jan 2009', '19 Jan 2009', '20 Jan 2009', '21 Jan 2009',
                        '22 Jan 2009', '25 Jan 2009', '26 Jan 2009', '27 Jan 2009', '28 Jan 2009',
                        '29 Jan 2009', '1 Feb 2009'],
            'change': [ -0.25, 0.06, -0.54, 0.72, 0.50, 
                         0.27, 0.33, 0.42, 0.24, -0.19,
                         0.14,-0.42,  0.67, 0.00,-0.28, 
                         0.03, 0.38, -0.19,-0.58, 0.57,
                         0.04,-0.54,0.74,-0.67,-0.43,
                         -1.33,0.15,0.04,0.35,-1.15,
                         -0.76, 0.47
            ]}
        output = [
                None, None, None, None, None, None, None, None, None, None, None, None, None, 
                70.52631578947368, 66.31643063803867, 66.54684209914029, 69.4019753809938, 
                66.35266035339271, 57.97824321264385, 62.92991023695419, 63.25711551042748, 
                56.06279393758636, 62.3774703182676, 54.71060328275266, 50.42679636683586, 
                39.995517169850004, 41.466160987898725, 41.875269179055124, 45.46684102650463, 
                37.30936292335553, 33.08472839167112, 37.77708101316913
            ]
        inputDf = pd.DataFrame(data = input)
        outputDf = pd.DataFrame(data = input)
        outputDf['rsi14'] = output
        self.assertTrue(RSI.compute(inputDf, 14).equals(outputDf))

        # # http://cns.bu.edu/~gsc/CN710/fincast/Technical%20_indicators/Relative%20Strength%20Index%20(RSI).htm
        input = {
            # Reversed of website for testing
            'date': [
                '13 Jan 2009', '12 Jan 2009', '11 Jan 2009', '8 Jan 2009', '7 Jan 2009', '6 Jan 2009',
                '5 Jan 2009', '4 Jan 2009', '31 Dec 2009', '30 Dec 2009', '29 Dec 2009', '28 Dec 2009',
                '24 Dec 2009', '23 Dec 2009', '22 Dec 2009', '21 Dec 2009', '18 Dec 2009', '17 Dec 2009',
                '16 Dec 2009'
            ],
            'change': [ -1.1875, 1.3125, 0.5000, -2.6250, -1.0000, -1.0000, 1.3750, 1.7500, -2.4375, 
                        -0.5625, -0.2500, 2.0625, 1.1250, 0.3750, -0.6875, -2.0000, 0.5000, -0.6875, 
                        1.0000]
        }
        output = [  43.992110594000444, 47.38184957507224, 42.863429113074524, 41.073449472180485,
                    48.47708511243952, 51.77865612648221, None, None, None, None, None, None, None,
                    None, None, None, None, None, None
            ]
        inputDf = pd.DataFrame(data = input)
        outputDf = pd.DataFrame(data = input)
        outputDf['rsi14'] = output
        self.assertTrue(RSI.compute(inputDf, 14).equals(Ordering.reverse(outputDf)))