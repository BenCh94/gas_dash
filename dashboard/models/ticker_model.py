""" The ticker model definition """
from django.db import models
from django.contrib.postgres.fields import JSONField


class Ticker(models.Model):
	""" Ticker model for the underlying stock/company referenced by users stocks """
	historical_data = JSONField(null=True)
	ticker = models.CharField(max_length=10, unique=True)
	logo_url = models.URLField(default='https://www.fillmurray.com/200/300')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.ticker
