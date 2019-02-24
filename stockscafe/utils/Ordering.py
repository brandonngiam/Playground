import stockscafe.utils.Conversion as Conversion

def byDate(df, ascending):
    # Makes a strong assumption that DataFrame is already sorted.
    # This is used to simply ensure Dates are either in Ascending order or Descending order
    if len(df.index) < 2: 
        return df
    dateTimeA = Conversion.string2DateTime(df.loc[0, 'date'])
    dateTimeB = Conversion.string2DateTime(df.loc[1, 'date'])
    if dateTimeA == dateTimeB: # Do nothing if equal
        return df 
    if ascending:
        if dateTimeA < dateTimeB:
            return df
        else: 
            return reverse(df)
    else:
        if dateTimeA > dateTimeB:
            return df
        else:
            return reverse(df)

def reverse(df):
    return df.iloc[::-1].reset_index().drop('index', 1)