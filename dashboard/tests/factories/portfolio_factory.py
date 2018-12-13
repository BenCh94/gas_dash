import factory
from ...models import Portfolio


class PortfolioFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = Portfolio

	data = '[{day1: "test"}]'
