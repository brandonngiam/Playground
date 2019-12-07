# Import Stocks Cafe API
from stockscafe.StocksCafeApi import StocksCafeApi
# Import Stocks Cafe helper functions
import lib
"""
Strategy Tester proof of concept
Author(s):
    Joe Ang
Description
    Strategy testing using BackTrader with StocksCafe API.
"""
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import datetime
# Import the backtrader platform
import backtrader as bt
from backtrader_plotting import Bokeh
from backtrader_plotting.schemes import Tradimo
cus_module_path = '../'
sys.path.append(cus_module_path)


class BreakoutBox(bt.Indicator):
    """
    Define indicator and strategy classes
    """
    alias = ('BBox')
    lines = ('top', 'bot')
    params = (
        # Window period for breakout
        ('breakout_period', 5),
        # How many dollars beyond period high/low to qualify for breakout.
        ('exceed_by', 0.1)
    )
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.lines.top = bt.indicators.Highest(
            self.data.high + self.p.exceed_by,
            period=self.p.breakout_period)
        self.lines.bot = bt.indicators.Lowest(
            self.data.low - self.p.exceed_by,
            period=self.p.breakout_period)


class TestStrategy(bt.Strategy):
    """
    Create a strategy
    """

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('{}, {}, {}'.format(self.datas[0]._name, dt.isoformat(), txt))
        print('{}, {}'.format(dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the high, low lines in the data[0] dataseries
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.dataclose = self.datas[0].close
        self.bbox = BreakoutBox()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])
        self.log('H {:.2f}, T {:.2f}, L {:.2f}, B {:.2f}'.format(
            self.datahigh[0], self.bbox.lines.top[0],
            self.datalow[0], self.bbox.lines.bot[0])
        )
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        try:
            if self.order:
                return
        except AttributeError:
            pass

        # Check if we are in the market
        if not self.position:
            order_validity = datetime.datetime.now()
            self.order = self.buy(exectype=bt.Order.StopLimit,
                                  price=self.bbox.lines.top,
                                  plimit=self.bbox.lines.top,
                                  valid=order_validity
                                  )

            # BUY, BUY, BUY!!! (with default parameters)
            self.log('BUY Stop Limit CREATE, %.2f' % self.bbox.lines.top[0])
        else:
            order_validity = datetime.datetime.now()
            # Already in the market ... we might sell
            self.order = self.sell(exectype=bt.Order.StopLimit,
                                   price=self.bbox.lines.bot,
                                   plimit=self.bbox.lines.bot,
                                   valid=order_validity
                                   )
            self.log('SELL Stop Limit CREATE, %.2f' % self.bbox.lines.bot[0])


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Get Stocks Cafe symbol prices
    symbols = [
        ('SGX', 'D05')
    ]
    sc = StocksCafeApi(api_key_file='api-key.txt')
    prices = []
    for (exchange, symbol) in symbols:
        symbol_price = lib.get_symbol_prices(sc, exchange, symbol,
                                             start_date='2018-04-01',
                                             end_date=None)
        symbol_price = symbol_price[['date',
                                     'open', 'high', 'low', 'close', 'volume']]
        data = bt.feeds.PandasData(dataname=symbol_price,
                                   datetime='date',
                                   nocase=True)
        # Add the Stocks Cafe symbol prices to Cerebro
        cerebro.adddata(data, name=symbol)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Run over everything
    cerebro.run()
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
