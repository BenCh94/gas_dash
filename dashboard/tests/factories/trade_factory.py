import factory
from datetime import datetime
from .stock_factory import StockFactory
from ...models import Trade


class TradeFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Trade

	stock = factory.SubFactory(StockFactory)
	date = factory.LazyFunction(datetime.now)
	trade_type = 'b'
	amount = 2
	fees_usd = 2.99
	avg_price = 100
