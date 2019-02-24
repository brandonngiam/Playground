import stockscafe.utils.Ordering as Ordering

def compute(df, lookback):
    df = Ordering.byDate(df, True) # Need dates to be ascending order
    ma = df['close'].rolling(lookback).mean()
    df[f'sma{lookback}'] = ma
    return df