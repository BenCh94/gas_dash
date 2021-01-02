import factory
from datetime import datetime
from ...models import Ticker


class TickerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticker

    name = 'test'
    ticker = 'DIS' # Needs a real ticker for testing requests