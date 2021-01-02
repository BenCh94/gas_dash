import factory
from datetime import datetime
from ...models import Stock
from .ticker_factory import TickerFactory 


class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stock

    ticker_data = factory.SubFactory(TickerFactory)
    name = 'test'
    ticker = 'DIS' # Needs a real ticker for testing requests
    quantity = 1
    invested = 10
    fees_usd = 2.99
    status = 'a'