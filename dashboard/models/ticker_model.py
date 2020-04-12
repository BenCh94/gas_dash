""" The ticker model definition """
from django.db import models
from django.contrib.postgres.functions import RandomUUID
from django.contrib.postgres.fields import JSONField


class Ticker(models.Model):
    """ Ticker model for the underlying stock/company referenced by users stocks """
    uuid = models.UUIDField(default=RandomUUID(), unique=True)
    historical_data = JSONField(null=True)
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=200, null=True)
    logo_url = models.URLField(default='https://www.fillmurray.com/200/300')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # API provided fields for refrence all nullable
    reference_date = models.DateTimeField(null=True)
    entity_type = models.CharField(max_length=10, null=True)
    provider_id = models.CharField(max_length=200, null=True)
    region = models.CharField(max_length=20, null=True)
    currency = models.CharField(max_length=5, null=True)
    active = models.BooleanField(default=True)
    figi = models.CharField(max_length=50, null=True)
    cik = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.ticker

    # @classmethod
    # def create_from_iex(cls, symbol)
