import requests
from datetime import date, timedelta, datetime
import random
import json
import os
import base64
import pandas as pd
from math import ceil
from scipy.stats import norm
from diskcache import Cache
#from stockscafe.StocksCafeApi import StocksCafeApi
#from StocksCafeApi import StocksCafeApi # Dev version of api
import logging
logger = logging.getLogger(__name__)


def generate_data(startDate, endDate, indexOffset=0):
    delta = endDate - startDate
    data=[]
    for i in range(delta.days + 1):
        d=startDate + timedelta(i)
        # Convert to string and remove leading zeroes
        dStr = d.strftime('%d %b %Y').lstrip('0')
        close = (10 + i + indexOffset) * random.random()
        high = close + random.random() * 2
        low = close - random.random() * close
        record={'date':dStr,'high': high,'low': low,'close': close}
        data.append(record)
    return data

def get_dividends(stocks_cafe, start_date, end_date, cachedir='cache'):
    os.chdir(os.path.dirname(__file__))
    cachename='get_dividends-{}-{}'.format(
        start_date, end_date
    )
    cachefile=os.path.join(os.getcwd(), cachedir, cachename)
    try:
        return readcache(cachefile)
    except FileNotFoundError:
        df = stocks_cafe.getCollectedDividends(start_date, end_date)
        writecache(df, cachefile)
    return df

def get_portfolio(stocks_cafe, label_id=None, open_only = True,
                    cachedir='cache', cache_ttl_mins=60):
    cache = Cache(cachedir)
    cache_key = "get_portfolio-{}".format(label_id)
    df = cache.get(cache_key)
    if df is None:
        results = stocks_cafe.getPortfolio(label_id = label_id,
                                            open_only = open_only)
        df = results['data']
        df['date'] = pd.to_datetime(results['eod_date'], format='%Y-%m-%d')
        cache.set(cache_key, df, expire = cache_ttl_mins * 60)
    return df

# Param
# - page: Integer or None. If None, get all pages
def get_portfolio_transactions_old(
    stocks_cafe, page=None, cachedir='cache', cache_ttl_mins=60):

    cache = Cache(cachedir)
    cache_key = "get_portfolio_transactions-{}".format(page)

    data = cache.get(cache_key)
    if data is None:
        if isinstance(page, int):
            # Fetch a single page
            results = stocks_cafe.getPortfolioTransactions(
                page = page)
            data = results['data']
        else:
            # Fetch all pages.

            # Get first page and see how many pages there are
            results = stocks_cafe.getPortfolioTransactions(page = 1)
            total_pages = results['total_pages']
            if total_pages > 1:
                # Fetch remaining pages
                dfs = []
                dfs.append(results['data'])
                for cur_page in range(2, total_pages + 1):
                    results = stocks_cafe.getPortfolioTransactions(
                            page = cur_page)
                    dfs.append(results['data'])
                data = pd.concat(dfs)
            else:
                # Only 1 page
                data = results['data']

        data['date_obj'] = pd.to_datetime(
            data['date'], format='%d %b %Y')
        data.sort_values('date_obj', inplace=True)
        data = data.reset_index(drop=True)
        cache.set(cache_key, data, expire = cache_ttl_mins * 60)
    return data

# Fetch as many records as possible between start_date and end_date
# start_date and end_date are datetime objects. Not strings.
def get_symbol_prices_single_call (
        stocks_cafe, exchange, symbol, start_date, end_date,
        cachedir='cache', cache_ttl_days=250):
    assert(start_date < end_date)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    cache = Cache(cachedir)
    cache_key = "get_prices_single_call-{}-{}-{}-{}".format(
                    exchange, symbol, start_date_str, end_date_str)
    df = cache.get(cache_key)
    if df is None:
        r = stocks_cafe.getPricesBetween(exchange, symbol,
                            start_date=start_date_str, end_date=end_date_str)
        df = r['eod_list']
        if df.empty:
            e = "[No data] get_prices_single_call({}, {},".format(
                    exchange, symbol)
            e += "{}, {})".format(start_date, end_date)
            logger.info('No prices')
            logger.debug(e)
        else:
            df['date_obj'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
            df = df.drop('date', axis=1).rename(columns={'date_obj': 'date'})
            df.sort_values('date', inplace=True)            
        cache.set(cache_key, df, expire = cache_ttl_days * 86400)
    return df

# Params:
# - end_date: a '%Y-%m-%d' string. Default is today.
# - start_date: a '%Y-%m-%d' string. Default is 60 days from end_date.
# Optimized cache writes and reads in batches.
def get_symbol_prices(stocks_cafe, exchange, symbol, start_date=None,
                        end_date=None, cachedir='cache', cache_ttl_days=1):
    default_record_count = 500
    date_format = '%Y-%m-%d'
    max_days_per_page = 1000
    if end_date:
        end_date = datetime.strptime(end_date, date_format)
    else:
        end_date = datetime.now()
    if start_date:
        start_date = datetime.strptime(start_date, date_format)
    else:
        start_date = end_date - timedelta(days = default_record_count)
    if end_date < start_date:
        tmp = start_date
        start_date = end_date
        end_date = tmp
    # Page the API calls into 1000 days each
    delta_days = (end_date - start_date).days
    pages = ceil(delta_days / max_days_per_page)
    #print(f"Pages: {pages}")
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    # Start retrieving from start_date
    dfs = []
    for d in range(0, pages):
        pg_start = start_date + timedelta(days = max_days_per_page * d)
        pg_end = pg_start + timedelta(days = max_days_per_page - 1)
        if pg_end > end_date:
            # This is the last page
            pg_end = end_date

        pg_start_str = pg_start.strftime("%Y-%m-%d")
        pg_end_str = pg_end.strftime("%Y-%m-%d")
        logger.debug('{} Page [{}]: {} to {}'.format(
                        symbol, d+1, pg_start_str, pg_end_str))
        df = get_symbol_prices_single_call (
                stocks_cafe, exchange, symbol, pg_start, pg_end)
        if df.empty:
            #print()
            lmsg = 'get_symbol_prices_single_call no data:'
            lmsg += '{}:{} {} to {}'.format(
                        exchange, symbol, pg_start, pg_end)
            logger.info(lmsg)
            pass
        else:
            dfs.append(df)

    retval = pd.concat(dfs)
    # Parse volume from thousands separated str to int
    #retval['volume'] = retval['volume'].str.replace(',', '')
    #retval['volume'] = pd.to_numeric(retval['volume']).fillna(0)
    # Order by date
    retval = retval.sort_values('date').reset_index(drop=True)
    return retval

# Fetch as many records as possible between start_date and end_date
# start_date and end_date are datetime objects. Not strings.
def get_portfolio_tx_single_call (
        stocks_cafe, start_date, end_date, label_id=None,
        cachedir='cache', cache_ttl_days=250):
    assert(start_date < end_date)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    cache = Cache(cachedir)
    cache_key = "get_port_tx_single_call-{}-{}-{}".format(
                    start_date_str, end_date_str, label_id)
    df = cache.get(cache_key)
    if df is None:
        r = stocks_cafe.getPortfolioTransactionsBetween(
                            start_date=start_date_str, end_date=end_date_str,
                            label_id=label_id)
        df = r['data']
        if df.empty:
            logger.info('Empty df')
        else:
            df['date_obj'] = pd.to_datetime(df['date'], format='%d %b %Y')
            df = df.drop('date', axis=1).rename(columns={'date_obj': 'date'})
            df.sort_values('date', inplace=True)            
        cache.set(cache_key, df, expire = cache_ttl_days * 86400)
    return df

# Params:
# - end_date: a '%Y-%m-%d' string. Default is today.
# - start_date: a '%Y-%m-%d' string. Default is 60 days from end_date.
# Optimized cache writes and reads in batches.
def get_portfolio_tx(stocks_cafe, start_date=None, end_date=None,
                        label_id=None,
                        cachedir='cache', cache_ttl_days=250):
    date_format = '%Y-%m-%d'
    max_days_per_page = 1000
    if end_date:
        end_date = datetime.strptime(end_date, date_format)
    else:
        end_date = datetime.now()
    if start_date:
        start_date = datetime.strptime(start_date, date_format)
    else:
        start_date = end_date - timedelta(days = default_record_count)
    if end_date < start_date:
        tmp = start_date
        start_date = end_date
        end_date = tmp
    # Page the API calls into 1000 days each
    delta_days = (end_date - start_date).days
    pages = ceil(delta_days / max_days_per_page)
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    # Start retrieving from start_date
    dfs = []
    for d in range(0, pages):
        pg_start = start_date + timedelta(days = max_days_per_page * d)
        pg_end = pg_start + timedelta(days = max_days_per_page - 1)
        if pg_end > end_date:
            # This is the last page
            pg_end = end_date
        
        pg_start_str = pg_start.strftime("%Y-%m-%d")
        pg_end_str = pg_end.strftime("%Y-%m-%d")
        logger.debug('Page [{}]: {} to {}'.format(
                        d+1, pg_start_str, pg_end_str))

        df = get_portfolio_tx_single_call (stocks_cafe, pg_start, pg_end,
                                            label_id = label_id)
        if df.empty:
            df.info('Empty df')
            pass
        else:
            dfs.append(df)
            #print('\tActual: {} to {}'.format(df.date.min(), df.date.max()))
    retval = pd.concat(dfs, sort=False)
    retval = retval.sort_values('date').reset_index(drop=True)
    return retval

def pagination_ref_recent_stock_prices(
        stocks_cafe, exchange, symbol, 
        page=None, cachedir='cache', cache_ttl_mins=60):

    today=datetime.now()
    today_str=today.strftime("%Y-%m-%d")

    cache = Cache(cachedir)
    cache_key = "get_stock_prices-{}-{}-{}-{}-{}".format(exchange, symbol,
                start_date, end_date, page)
    data = cache.get(cache_key)
    if data is None:
        if isinstance(page, int):
            # Fetch a single page
            stocks_cafe.getPrices(self, exchange, symbol, page = 1)
            results = stocks_cafe.getPrices(
                exchange, symbol, start_date = start_date,
                end_date = end_date, page = page)
            data = results['eod_list']
        else:
            # Fetch all pages.

            # Get first page and see how many pages there are
            results = stocks_cafe.getPrices(exchange, symbol, page = 1)
            total_pages = results['total_pages']
            #print(f"get_prices pages: {total_pages}")
            if total_pages > 1:
                # Fetch remaining pages
                dfs = []
                dfs.append(results['eod_list'])
                for cur_page in range(2, total_pages + 1):
                    results = stocks_cafe.getPrices(
                                exchange, symbol, start_date = start_date,
                                end_date = end_date, page = cur_page)

                    dfs.append(results['eod_list'])
                data = pd.concat(dfs)
            else:
                # Only 1 page
                data = results['eod_list']

        data['date_obj'] = pd.to_datetime(
            data['date'], format='%d %b %Y')
        data.sort_values('date_obj', inplace=True)
        data = data.reset_index(drop=True)
        cache.set(cache_key, data, expire = cache_ttl_mins * 60)
    return data

# Variance-Covariance calculation of Value-at-Risk
# using confidence level c, with mean of returns mu
# and standard deviation of returns sigma.
def var_cov_var(c, mu, sigma):
    daily_var = -(norm.ppf(1-c, mu, sigma))
    # Convert daily to monthly VaR
    # https://www.investopedia.com/articles/04/101304.asp
    monthly_var = 4.472136 * daily_var
    return monthly_var

# Returns a df of monthly Value at Risk (VaR) in % for one symbol
# Original df is not changed.
# Params:
#   - df: dataframe of daily prices with 'date' and 'close'
#   - var_lookback: days to look back when calculating VaR
def calc_var(input_df, var_lookback, min_periods=None, confidence=0.99):
    df = input_df.copy()
    df.sort_values('date', inplace=True)
    df['returns'] = df['close'].pct_change()
    # Calculate rolling VaR for every month
    r = df.rolling(var_lookback, min_periods = min_periods)
    df['mean'] = r.returns.mean()
    df['stdev'] = r.returns.std()
    df['var_monthly'] = df.apply(
        lambda row: var_cov_var(confidence, row['mean'], row['stdev']), axis=1)
    df = df[df['var_monthly'].isnull() != True].sort_values('date')
    return df

# Converts portfolio dataframe to one row indexed by date with all
# symbols as columns
# Returns a dataframe with only 1 row. Index is from 'date' column.
# Params:
# - df: portfolio dataframe to convert
# - row_date: the 'date' column value. Type is pandas.Timestamp.
def flatten_portfolio(df):
    pf_date = (df['date'].iloc[0]) #.date()
    df['total_value'] = df['average_price'] * df['shares']
    df['exch-sym'] = list(zip(df['exchange'], df['symbol']))
    df = df[['shares', 'total_value', 'exch-sym']]
    df = df.rename(columns={'exch-sym':'symbol'})
    df.set_index(['symbol'], inplace=True)
    df = df.stack()
    df.index.set_names(['symbol','attribute'], inplace=True)
    df = df.to_frame()
    df.columns=['value']
    df = df.T.reset_index(drop=True)
    df['date'] = pf_date
    df = df.set_index('date')
    return df

# Converts transaction dataframe to one row indexed by date with all
# symbols as columns.
# Multiple transactions within same day and same symbol is consolidated
# into one row.
# E.g.
# date | symbol | type | total_value | shares
# 10th | ABC    | BUY  | 1000        | 100
# 10th | ABC    | SELL | 2000        | 200
# Consolidated result:
# 10th | ABC    | BUY  | -1000       | -100

# Also converts all buy transactions to negative total_value and shares
# for cumulative summing later.
# E.g. 
# 10th | ABC    | BUY  | 1500       | 100
# Becomes
# 10th | ABC    | BUY  | -1500      | -100

# Returns a dataframe with multiple rows. Index is from 'date' column.
# Params:
# - df: transaction dataframe to convert
def flatten_transactions(df, cachedir='cache', cache_ttl_mins=60):
    cache = Cache(cachedir)
    cache_key = "transaction_df_to_row"
    data = cache.get(cache_key)
    if data is None:
        df['date_obj'] = pd.to_datetime(df['date'], format='%d %b %Y')
        # Convert all buy transactions to negative total_value and shares
        # for latest first cumulative summing later
        buy = df[df['type']=='BUY'][['total_value', 'shares']] * -1
        # Update back to transactions. Replaces matching index.
        df.update(buy)
        # Consolidate all date-exchange-symbol transactions into one row.
        group_cols = ['date_obj', 'exchange', 'symbol']
        g = df.groupby(group_cols)['total_value', 'shares'].sum()
        g = g.reset_index()
        # Combines exchange and symbol into a tuple so
        # that it's easier to stack into (exchange,symbol) columns later.
        g['exch-sym'] = list(zip(g['exchange'], g['symbol']))
        g = g[['date_obj', 'exch-sym', 'total_value', 'shares']]
        g.rename(columns={'exch-sym':'symbol'}, inplace=True)
        # Group transactions by day so we can stack the symbols
        # into columns.
        g = g.groupby(['date_obj'])
        day_txs = []
        for date_obj, day_df in g:
            day_df = day_df[['symbol', 'total_value', 'shares']]
            day_df.set_index('symbol', inplace=True)
            day_df = day_df.stack()
            day_df.index.set_names(['symbol','attribute'], inplace=True)
            day_df = day_df.to_frame()
            day_df.columns=['value']
            day_df = day_df.T.reset_index(drop=True)
            day_df['date'] = date_obj#.date()
            day_df = day_df.set_index('date')
            day_txs.append(day_df)
        data = pd.concat(day_txs)
        cache.set(cache_key, data, expire = cache_ttl_mins * 60)
    return data

# Returns a dataframe with multiple rows. Index is from 'date' column.
# Params:
# - df: VaR dataframe to convert
def var_df_to_row(df, cachedir='cache', cache_ttl_mins=60):
    # Group transactions by day so we can stack the symbols
    # into columns.
    cache = Cache(cachedir)
    cache_key = "var_df_to_row"
    data = cache.get(cache_key)
    if data is None:
        g = df.groupby(['date'])
        day_vars = []
        for date_obj, day_df in g:
            day_df = day_df[['symbol', 'var_monthly']]
            day_df.set_index('symbol', inplace=True)
            day_df = day_df.stack()
            day_df.index.set_names(['symbol', 'attribute'], inplace=True)
            day_df = day_df.to_frame()
            day_df.columns=['value']
            day_df = day_df.T.reset_index(drop=True)
            day_df['date'] = date_obj
            day_df = day_df.set_index('date')
            day_vars.append(day_df)
        data = pd.concat(day_vars)
        cache.set(cache_key, data, expire = cache_ttl_mins * 60)
    return data

####### Need to get prices/var of syms that are in portf but not in tx. E.g. T82U
# It is in portf, but last transaction was out of date range specified.
# Right approach is to get prices from hist, not before.


# Returns a Dataframe of OHLC prices and VaR per sym day. E.g
#   change change_percent  close currency  high    low   open     volume \
#1   0.010          0.70%  1.435      SGD  1.44  1.415  1.415  1,901,000 
#2  -0.005         -0.35%  1.430      SGD  1.44  1.430  1.430  1,039,000 
#
#      date   returns      mean     stdev  var_monthly       symbol  
#2014-07-11  0.007018  0.000671  0.008160     0.081896  (SGX, ME8U)  
#2014-07-14 -0.003484  0.000638  0.008136     0.081791  (SGX, ME8U)  
#
# Parameters
# - date_range: Dataframe of structure:
#             start_date   end_date
# exch-sym                         
# (SGX, ME8U) 2018-02-19 2019-04-30
# (SGX, T82U) 2019-04-30 2019-04-30
# Output: Dataframe
# For each symbol, fetch prices from (oldest 'date' - var_lookback * 2)
# till today.
# Does not modify src_df by making a copy of it.

def get_prices_vars(stocks_cafe, date_range, var_lookback, var_min_periods, 
                    var_confidence):
    # Get all symbols and their date ranges
    
    # Fetch price for each symbol.
    # Start from (earliest transaction date - porfolio lookback)
    var_dfs = []
    for (exch, sym), d in date_range.to_dict(orient='index').items():
        # Fetch prices 2 x var_lookback ago as
        # actual number of trading days < var_lookback
        p_start = d['start_date'] - timedelta(days = var_lookback * 2)
        p_start_str = p_start.strftime('%Y-%m-%d')
        p_end_str = d['end_date'].strftime('%Y-%m-%d')
        lmsg = 'Fetch prices for '
        lmsg+= '{}:{} > {} to {}, latest first.'.format(
            exch, sym, p_start_str, p_end_str)
        logger.info(lmsg)
        p = get_symbol_prices(stocks_cafe, exch, sym,
                            start_date = p_start_str, end_date = p_end_str)
        #print(f"###### fetched prices for ({sym}), latest first #########")
        logger.debug(p.sort_values('date', ascending=False))
        # Calculate VaR for this symbol
        var_df = calc_var(p, var_lookback, min_periods = var_min_periods,
                                confidence = var_confidence)
        if var_df.empty:
            logger.info("[No VaR] {}:{}|{} > {}".format(
                            exch, sym, p_start_str, p_end_str))
        else:
            var_df['symbol'] = [(exch, sym)] * len(var_df)
            var_dfs.append(var_df)

    return(pd.concat(var_dfs))

# From portfolio and portfolio transactions, returns Dataframe of 
def get_price_date_range(portfolio, portfolio_transactions):
    common_cols = ['date', 'exchange', 'symbol', 'currency']
    pf = portfolio[common_cols]
    pf_tx = portfolio_transactions[common_cols]
    merged = pd.concat([pf, pf_tx])
    merged['exch-sym'] = list(zip(merged['exchange'], merged['symbol']))
    merged = merged.groupby('exch-sym').agg({'date': ['min', 'max']})
    merged.columns = merged.columns.droplevel()
    merged.rename(columns={'min':'start_date', 'max':'end_date'}, inplace=True)
    return merged

# From portfolio history df, add a new column called 'total_value'
# This is the value of the portfolio on that day.
def get_portfolio_value(df):
    daily_pf_value = df.sum(level='attribute', axis=1)[['total_value']]
    daily_pf_value.rename(columns={'total_value': 'sub_total'}, inplace=True)
    # Add an artificial 2nd level column index so the join with hist will
    # not result in flattened column levels.
    daily_pf_value.columns = pd.MultiIndex.from_product(
                                    [daily_pf_value.columns, ['total_value']])
    return (df.join(daily_pf_value, how='left'))

# From portfolio history df,
# add a new column under each symbol called "weight".
# Weight = value of the symbol / total value of portfolio
def get_portfolio_symbol_weights(df):
    symbols = list(df.columns.levels[0])
    for symbol in symbols:
        df[symbol, 'weight'] = (
            df[symbol, 'total_value'] / df['sub_total', 'total_value']
        )
    return df

# Get re-ordered indices of elements in old based on element sequence in new.
# If append_not_found_to_back is True,
#   Elements in new not found in old are:
#       1. Given an index starting from last old index +1.
#       2. Appended to end of new sequence.
# Else, elements in new not found in old are dropped.
def reorder_index (old, new, append_not_found_to_back=False):
    found = []
    not_found = []
    # Missing index start from old's last index + 1,
    # which is effectively length of old
    missing_index = len(old)
    for n in new:
        try:
            old_index = old.index(n)
            found.append(old_index)
        except ValueError:
            not_found.append(missing_index)
            missing_index += 1

    if append_not_found_to_back:
        found.extend(not_found)
    return found
