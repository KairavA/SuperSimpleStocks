import unittest
from models import GlobalBeverageCorporationExchange, CommonStock, PreferredStock, Trade, ACTION, SYMBOL
import random
import datetime
import logging

logger = logging.getLogger(__name__)


class TestGlobalBeverageCorporationExchange(unittest.TestCase):

    def test_stock(self):
        GBCE_object = GlobalBeverageCorporationExchange()
        stock = CommonStock(SYMBOL.TEA, 2, 0, 100)
        dividend = stock.dividend_yield(10)
        self.assertEqual(dividend, 0.2)
        pe = stock.pe_ratio(10)
        self.assertEqual(pe, 5)
        with self.assertRaises(ValueError):
            stock.dividend_yield(0)
        with self.assertRaises(ValueError):
            stock.pe_ratio(0)

        stock = PreferredStock(SYMBOL.GIN, 8, 2, 100)
        dividend = stock.dividend_yield(10)
        self.assertEqual(dividend, 20)
        with self.assertRaises(ValueError):
            stock.dividend_yield(0)


    def test_exchange(self):
        GBCE_object = GlobalBeverageCorporationExchange()
        stock = CommonStock(SYMBOL.TEA, 2, 0, 100)
        trade = GBCE_object.record_trade(stock, 100, ACTION.BUY, 11.0)
        trade = GBCE_object.record_trade(stock, 100, ACTION.BUY, 11.0)
        self.assertTrue(isinstance(trade, Trade))
        saved_transaction = GBCE_object.get_recent_trades()[0]
        self.assertEqual(trade.Stock.Symbol, saved_transaction.Stock.Symbol)

    def test_all_share_index(self):
        GBCE_object = GlobalBeverageCorporationExchange()
        stocks = [CommonStock(SYMBOL.TEA, 0, 0, 100), CommonStock(SYMBOL.POP, 8, 0, 100), CommonStock(SYMBOL.ALE, 23, 0, 60),
                  PreferredStock(SYMBOL.GIN, 8, 2, 100), CommonStock(SYMBOL.JOE, 13, 0, 250)]

        for stock in stocks:
            for i in range(1, 20):
                trade = GBCE_object.record_trade(stock, random.randint(100, 1000), random.choice(list(ACTION)),
                                                 random.random() * random.randint(100,500))
                trade.TimeStamp = (datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0, 10)))\
                    .timestamp()

        all_share_index = GBCE_object.get_all_share_index()
        self.assertIsNotNone(all_share_index)
        for stock in stocks:
            vwsp = GBCE_object.volume_weighted_stock_price(symbol=stock.Symbol, time_gap_minutes=5)
            self.assertIsNotNone(vwsp)


if __name__ == '__main__':
    unittest.main()