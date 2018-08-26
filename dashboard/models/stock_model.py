import datetime

from django.db import models
from django.utils import timezone
from .trade_model import Trade

class Stock(models.Model):
	StockStatuses = [('a', 'Active'), ('i', 'Inactive')]
	user_profile = models.ForeignKey('dashboard.Profile', on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	ticker = models.CharField(max_length=10)
	quantity = models.FloatField(blank=True, null=True)
	invested = models.FloatField(blank=True, null=True)
	fees_usd = models.FloatField(blank=True, null=True)
	start_date = models.DateField(blank=True, null=True)
	status = models.CharField(max_length=2, choices=StockStatuses)
	def __str__(self):
		return self.name

	def trades(self):
		trades = Trade.objects.filter(stock = self)
		if trades.count() > 0:
			return trades.order_by('date')
		else:
			return 'None'

	def get_ticker(self):
		return self.ticker		