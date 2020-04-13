""" The ticker model definition """
import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField


class Ticker(models.Model):
    """ Ticker model for the underlying stock/company referenced by users stocks """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    historical_data = JSONField(null=True, blank=True)
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=200, null=True)
    logo_url = models.URLField(default='https://www.fillmurray.com/200/300')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # API provided fields for refrence all nullable
    reference_date = models.DateField(null=True, blank=True)
    entity_type = models.CharField(max_length=10, null=True, blank=True)
    provider_id = models.CharField(max_length=200, null=True, unique=True, blank=True)
    region = models.CharField(max_length=20, null=True, blank=True)
    currency = models.CharField(max_length=5, null=True, blank=True)
    active = models.BooleanField(default=True)
    figi = models.CharField(max_length=50, null=True, unique=True, blank=True)
    cik = models.CharField(max_length=50, null=True, unique=True, blank=True)

    class Meta:
        unique_together = ('ticker', 'name', 'region')

    def __str__(self):
        return self.ticker

    @classmethod
    def create_from_iex(cls, symbol):
        """ Create ticker object from IEX api data """
        ticker_model = {
            'ticker': symbol['symbol'],
            'name': symbol['name'],
            'reference_date': symbol['date'],
            'entity_type': symbol['type'],
            'provider_id': symbol['iexId'],
            'region': symbol['region'],
            'currency': symbol['currency'],
            'active': symbol['isEnabled'],
            'figi': symbol['figi'],
            'cik': symbol['cik']}
        return cls(**ticker_model)
