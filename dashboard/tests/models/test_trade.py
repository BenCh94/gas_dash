from django.test import TestCase
from django.shortcuts import get_object_or_404
from ..factories import UserFactory, StockFactory, TradeFactory
from ...models import Stock, Trade


class TradeTestCase(TestCase):
	def setUp(self):
		user = UserFactory.create()
		stock = StockFactory.create(user_profile=user.profile)
		trade = TradeFactory.create(stock=stock)

	def test_trade_string(self):
		trade = Trade.objects.first()

		self.assertEqual(str(trade), f'{trade.trade_type}: {trade.amount} @ {trade.avg_price} - {trade.date}')
