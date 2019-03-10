from ...utils import Ordering
from ..momentum import MovingAverage
import numpy as np

def compute(df, window, window2):
    # %K = (Current Close - Lowest Low)/(Highest High - Lowest Low) * 100
    df = Ordering.byDate(df, True) # Need dates to be ascending order
    output_values = []
    for _ in range(window - 1): # fill windows - 1 with nan
        output_values.append(np.nan)
    for i in range(window - 1, len(df), 1):
        close = df['close'][i]
        high = df.loc[i-window+1:i, 'high']
        max_high = max(high)
        low = df.loc[i-window+1:i, 'low']
        min_low = min(low)
        v = (close - min_low) / (max_high - min_low) * 100
        output_values.append(v)
    df[f'%K{window}'] = output_values

    dValues = MovingAverage.computeSmaGivenList(df[f'%K{window}'], window2)
    df[f'%D{window2}'] = dValues
    return df


