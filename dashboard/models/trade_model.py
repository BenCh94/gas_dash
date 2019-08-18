import datetime

from django.db import models
from django.utils import timezone

class Trade(models.Model):
	TradeTypes = [('b', 'Buy'), ('s','Sell')]
	stock = models.ForeignKey('dashboard.Stock', on_delete=models.CASCADE)
	date = models.DateField()
	trade_type = models.CharField(max_length=2, choices=TradeTypes)
	amount = models.FloatField()
	fees_usd = models.FloatField()
	avg_price = models.FloatField()
	def __str__(self):
		return f'{self.trade_type}: {self.stock.ticker}, {self.date}'
