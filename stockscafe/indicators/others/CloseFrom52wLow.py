import pandas as pd
# Close % From 52-Weeks Low = ('Last Close' - '52W Low') x 100 / ('52W High' - '52W Low')
# Params
# 1) df: dataframe of prices
# 2) window: number of weeks to look back
def compute(df, window=52):
    windowDays=window*5 # Data feed exclude weekends
    # Convert date to date time object to sort
    df['date_dt']=pd.to_datetime(df['date'], format='%d %b %Y') #22 Mar 2019
    df=df.sort_values('date_dt').reset_index().drop(['index', 'date_dt'], axis=1)
    # Compute rolling <window> weeks
    windowLowCol = f'{window}w_low'
    windowHighCol = f'{window}w_high'
    windowResultCol=f'{window}w_close_percent'
    df[windowLowCol]=df.low.rolling(windowDays, min_periods=None).min()
    df[windowHighCol]=df.high.rolling(windowDays, min_periods=None).max()
    df[windowResultCol]=100*(df['close']-df[windowLowCol]) / (df[windowHighCol]-df[windowLowCol])
    return df