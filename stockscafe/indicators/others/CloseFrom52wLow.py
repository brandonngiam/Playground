'''
Line max length 79:
0123456789012345678901234567890123456789012345678901234567890123456789012345678
'''
import pandas as pd
# Close % From 52-Weeks Low = ('Last Close' - '52W Low') x 100 / ('52W High' - '52W Low')
# Params
# 1) df: dataframe of prices
# 2) window: number of weeks to look back
def compute(df, window=52):
    window_days=window*5 # Data feed exclude weekends
    # Convert date to date time object to sort
    df['date_dt'] = pd.to_datetime(
        df['date'], format='%d %b %Y')
    df = df.sort_values('date_dt').reset_index().drop(
        ['index', 'date_dt'], axis=1)
    # Compute rolling <window> weeks
    window_low_col = f'{window}w_low'
    window_high_col = f'{window}w_high'
    window_result_col = f'{window}w_close_percent'
    df[window_low_col] = df.low.rolling(window_days, min_periods=None).min()
    df[window_high_col] = df.high.rolling(window_days, min_periods=None).max()
    df[window_result_col] = (
                                df['close'] - df[window_low_col]
                            ) * 100 / (
                                df[window_high_col] - df[window_low_col]
                            )
    return df
