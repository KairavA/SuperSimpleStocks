import datetime
import logging
import numpy as np
import abc
from enum import Enum
import utils

logger = logging.getLogger(__name__)


class ACTION(Enum):
    BUY = "BUY"
    SELL = "SELL"


class SYMBOL(Enum):
    TEA = "TEA"
    POP = "POP"
    ALE = "ALE"
    GIN = "GIN"
    JOE = "JOE"


class Trade(object):

    def __init__(self, stock, quantity, action, price):
        self.Stock = stock
        self.Quantity = quantity
        self.Action = action
        self.Price = price
        self.TimeStamp = datetime.datetime.utcnow().timestamp()


class Stock(abc.ABC):

    def __init__(self, stock_symbol, last_divided, fixed_dividend, par_value):
        self.Symbol = stock_symbol
        self.LastDividend = last_divided
        self.FixedDividend = fixed_dividend
        self.ParValue = par_value

    @abc.abstractmethod
    def dividend_yield(self, price):
        pass

    @utils.nonZeroPrice
    def pe_ratio(self, price):
        return price/self.LastDividend if self.LastDividend else 0


class CommonStock(Stock):

    @utils.nonZeroPrice
    def dividend_yield(self, price):
        return self.LastDividend/price


class PreferredStock(Stock):

    @utils.nonZeroPrice
    def dividend_yield(self, price):
        return (self.FixedDividend * self.ParValue) / price


class GlobalBeverageCorporationExchange(object):

    def __init__(self):
        self._AllTrades = []

    def record_trade(self, stock, quantity, action, price):
        try:
            trade = Trade(stock, quantity, action, price)
            self._AllTrades.append(trade)
            return trade
        except Exception as ex:
            logger.error(f"Error when recording the trade with values: {stock.Symbol}, {quantity}, {action}, {price}")
            logger.error(ex)
            raise ex

    def get_recent_trades(self, symbol=None, time_gap_minutes=None):
        last_time_stamp = (datetime.datetime.utcnow() - datetime.timedelta(minutes=time_gap_minutes)).timestamp() if \
            time_gap_minutes else None
        return [trade for trade in self._AllTrades if ((not last_time_stamp) or trade.TimeStamp >
                last_time_stamp) and ((not symbol) or trade.Stock.Symbol == symbol)]

    def get_all_share_index(self):
        all_share_index = 0
        traded_stocks = set(transaction.Stock for transaction in self._AllTrades)
        if traded_stocks:
            vw_all_stocks = np.array([self.volume_weighted_stock_price(symbol=stock.Symbol) for stock in traded_stocks])
            all_share_index = vw_all_stocks.prod() ** (1.0 / len(traded_stocks))
            logger.info(f"all_share_index:{all_share_index}")
        return all_share_index

    def volume_weighted_stock_price(self, symbol=None, time_gap_minutes=None):
        vwsp = 0
        recent_trades = self.get_recent_trades(symbol, time_gap_minutes)
        if recent_trades:
            total_value = sum((trade.Quantity*trade.Price) for trade in recent_trades)
            total_quantity = sum(trade.Quantity for trade in recent_trades)
            vwsp = total_value/total_quantity
            logger.info(f"vwsp for {symbol}:{vwsp}")
        return vwsp
