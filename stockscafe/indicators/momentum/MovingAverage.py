from ...utils import Ordering
import numpy as np

def compute(df, lookback):
    df = Ordering.byDate(df, True) # Need dates to be ascending order
    ma = df['close'].rolling(lookback).mean()
    df[f'sma{lookback}'] = ma
    return df

def computeExponential(df, lookback):
    df = Ordering.byDate(df, True) # Need dates to be ascending order
    ema = numpy_ewma_vectorized_v2(df['close'], lookback)
    df[f'ema{lookback}'] = ema
    return df

# https://stackoverflow.com/questions/42869495/numpy-version-of-exponential-weighted-moving-average-equivalent-to-pandas-ewm
def numpy_ewma_vectorized_v2(data, window):
    alpha = 2 /(window + 1.0)
    alpha_rev = 1-alpha
    n = data.shape[0]

    pows = alpha_rev**(np.arange(n+1))

    scale_arr = 1/pows[:-1]
    offset = data[0]*pows[1:]
    pw0 = alpha*alpha_rev**(n-1)

    mult = data*pw0*scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums*scale_arr[::-1]
    for i in range(int(window + window/2)): # first X elements are not stable
        out[i] = np.nan
    return out