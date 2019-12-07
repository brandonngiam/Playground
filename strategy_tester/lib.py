from datetime import date, timedelta, datetime
import pandas as pd
from math import ceil
from diskcache import Cache
import logging
logger = logging.getLogger(__name__)


# Fetch as many records as possible between start_date and end_date
# start_date and end_date are datetime objects. Not strings.
def get_symbol_prices_single_call(
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
                                         start_date=start_date_str,
                                         end_date=end_date_str)
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
        cache.set(cache_key, df, expire=cache_ttl_days*86400)
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
        start_date = end_date - timedelta(days=default_record_count)
    if end_date < start_date:
        tmp = start_date
        start_date = end_date
        end_date = tmp
    # Page the API calls into 1000 days each
    delta_days = (end_date-start_date).days
    pages = ceil(delta_days/max_days_per_page)
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    # Start retrieving from start_date
    dfs = []
    for d in range(0, pages):
        pg_start = start_date + timedelta(days=max_days_per_page*d)
        pg_end = pg_start + timedelta(days=max_days_per_page-1)
        if pg_end > end_date:
            # This is the last page
            pg_end = end_date

        pg_start_str = pg_start.strftime("%Y-%m-%d")
        pg_end_str = pg_end.strftime("%Y-%m-%d")
        logger.debug('{} Page [{}]: {} to {}'.format(
                        symbol, d+1, pg_start_str, pg_end_str))
        df = get_symbol_prices_single_call(
                stocks_cafe, exchange, symbol, pg_start, pg_end)
        if df.empty:
            lmsg = 'get_symbol_prices_single_call no data:'
            lmsg += '{}:{} {} to {}'.format(
                        exchange, symbol, pg_start, pg_end)
            logger.info(lmsg)
            pass
        else:
            dfs.append(df)

    retval = pd.concat(dfs)
    retval = retval.sort_values('date').reset_index(drop=True)
    return retval
