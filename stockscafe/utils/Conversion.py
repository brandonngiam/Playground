import pandas as pd
from . import Ordering
from datetime import datetime

def shiftTimeFrame(df, lookback):
    df = Ordering.byDate(df, False) # Need dates to be in descending order
    _list = []
    totalLength = len(df.index)
    for i in range(0, totalLength, lookback):
        endIndex = i+lookback-1
        if endIndex >= totalLength:
            break
        _high = max(df.loc[i:endIndex, 'high'])
        _low = min(df.loc[i:endIndex, 'low'])
        _open = df.loc[endIndex, 'open']
        _close = df.loc[i, 'close']
        _volume = sum([int(v.replace(',', '')) for v in df.loc[i:endIndex, 'volume']])
        _date = df.loc[i, 'date']
        _list.append([_high, _low, _open, _close, _volume, _date])
    return pd.DataFrame(_list, columns=['high', 'low', 'open', 'close', 'volume', 'date'])

def monthValue2ShortMonthString(value):
    return {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec'
    }.get(value, 'Unknown')  

def string2DateTime(str):
    # https://stackabuse.com/how-to-format-dates-in-python/
    return datetime.strptime(str, '%d %b %Y') # expected format 23 Feb 2019
