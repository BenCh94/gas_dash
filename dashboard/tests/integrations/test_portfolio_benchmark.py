from django.test import TestCase
from django.shortcuts import get_object_or_404
from ..factories import UserFactory, StockFactory, TradeFactory
from ...models import Stock, Trade
from ..portfolio_data_cleaning import PortfolioUpdate
from datetime import datetime

# Building the test case for complex portfolio updates
# Management command should first get updates for stocks/benchmarks.
# Given trades and chart data, test the PortfolioUpdate object returns the correct values.
class PortfolioUpdateTest(TestCase):
	""" The portfolio update test case """
	def setup(self):
		user = UserFactory.create()
		stock_1 = StockFactory.create(ticker='DIS', name='Disney', quantity=0, invested=0, fees_usd=0, status='a')
		stock_2 = StockFactory.create(ticker='TWTR', name='Twitter', quantity=0, invested=0, fees_usd=0, status='a')
		stock_3 = StockFactory.create(ticker='MTCH', name='Match', quantity=0, invested=0, fees_usd=0, status='a')
		trade_1 = TradeFactory.create(stock=stock_2, date=datetime.strptime('2018-02-08', '%Y-%m-%d'), amount=5, avg_price=16.54)
		trade_2 = TradeFactory.create(stock=stock_2, date=datetime.strptime('2018-07-27', '%Y-%m-%d'), amount=5, avg_price=34.75)
		trade_3 = TradeFactory.create(stock=stock_3, date=datetime.strptime('2018-02-09', '%Y-%m-%d'), amount=5, avg_price=34.98)
		trade_4 = TradeFactory.create(stock=stock_1, date=datetime.strptime('2018-04-05', '%Y-%m-%d'), amount=2, avg_price=101.48)

	# def test_portfolio_update_return_trade_df(self)

