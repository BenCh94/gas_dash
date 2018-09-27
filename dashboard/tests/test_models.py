from django.test import TestCase
from django.shortcuts import get_object_or_404
from .factories import *
from ..models import Stock, Trade, Portfolio, Profile, User


class StockTestCase(TestCase):
	def setUp(self):
		user = UserFactory.create()
		stock = StockFactory.create(user_profile=user.profile)
		stock2 = StockFactory.create(user_profile=user.profile, name='testnotrades')
		trade = TradeFactory.create(stock=stock)

	def test_stock_str(self):
		stock = get_object_or_404(Stock, name='test')

		self.assertEqual(str(stock), stock.name)

	def test_stock_ticker(self):
		stock = get_object_or_404(Stock, name='test')

		self.assertEqual(stock.get_ticker(), stock.ticker)

	def test_stock_trades(self):
		stock = get_object_or_404(Stock, name='test')
		stock2 = get_object_or_404(Stock, name='testnotrades')

		self.assertEqual(stock.trades().count(), 1)
		self.assertEqual(stock2.trades(), None)


class TradeTestCase(TestCase):
	def setUp(self):
		user = UserFactory.create()
		stock = stock = StockFactory.create(user_profile=user.profile)
		trade = TradeFactory.create(stock=stock)

	def test_trade_string(self):
		trade = Trade.objects.first()

		self.assertEqual(str(trade), trade.trade_type)