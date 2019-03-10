from ...utils import Ordering
import numpy as np

def compute(df, window):
    df = Ordering.byDate(df, True) # Need dates to be ascending order
    df[f'sma{window}'] = computeSmaGivenList(df['close'], window)
    return df

def computeExponential(df, window):
    df = Ordering.byDate(df, True) # Need dates to be ascending order
    df[f'ema{window}'] = computeEmaGivenList(df['close'], window)
    return df

def computeSmaGivenList(data, window):
    return data.rolling(window).mean()

# https://stackoverflow.com/questions/42869495/numpy-version-of-exponential-weighted-moving-average-equivalent-to-pandas-ewm
def computeEmaGivenList(data, window):
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
    for i in range(int(window + window/2)): # first (window + window/2) elements are not stable
        out[i] = np.nan
    return out