import factory
from datetime import datetime
from ..models import *


class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User

	username = factory.Sequence(lambda n: 'testuser{0}'.format(n))
	email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))


class StockFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Stock

	name = 'test'
	ticker = 'aaa'
	quantity = 1
	invested = 10
	fees_usd = 2.99
	status = 'a'

class TradeFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Trade

	stock = factory.SubFactory(StockFactory)
	date = factory.LazyFunction(datetime.now)
	trade_type = 'b'
	amount = 2
	fees_usd = 2.99
	avg_price = 100