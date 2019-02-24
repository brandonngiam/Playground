# https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:relative_strength_index_rsi
# RSI = 100 - (100 / 1 + RS)
# RS = AverageGain / AverageLoss
from typing import List
import stockscafe.utils.Ordering as Ordering

def compute(df, lookback):
    df = Ordering.byDate(df, True) # Need dates to be ascending order
    change_list = df['change']
    # Change list should be sorted with earlier change to latest change
    total_gain: int = 0.0
    total_loss: float = 0.0
    rsi_list: List[float] = []
    # Pad with None for first lookback - 1
    for i in range(lookback - 1):
        rsi_list.append(None)

    # First RSI
    for i in range(lookback):
        change: float = float(change_list[i])
        if change > 0:
            total_gain += change
        elif change < 0:
            total_loss += abs(change)
    average_gain = total_gain / lookback
    average_loss = total_loss / lookback
    rs = average_gain / average_loss
    rsi = 100 - (100 / (1 + rs))
    rsi_list.append(rsi)

    # Subsequent RSI
    for i in range(lookback,len(df.index)):
        change = float(change_list[i])
        if change > 0:
            average_gain = (average_gain * (lookback-1) + change) / lookback
            average_loss = (average_loss * (lookback-1)) / lookback
        elif change < 0:
            average_gain = (average_gain * (lookback-1)) / lookback
            average_loss = (average_loss * (lookback-1) + abs(change)) / lookback
        else:
            average_gain = (average_gain * (lookback-1)) / lookback
            average_loss = (average_loss * (lookback-1)) / lookback
        rs = average_gain / average_loss
        rsi = 100 - (100 / (1 + rs))
        rsi_list.append(rsi)
    df[f'rsi{lookback}'] = rsi_list
    return df
