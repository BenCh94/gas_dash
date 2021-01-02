""" The user stock model definition refers to a specific """
""" users stock. Ticker model contains overall company data """
import uuid
from django.db import models
from django.contrib.postgres.functions import RandomUUID
from .trade_model import Trade
from .ticker_model import Ticker

class Stock(models.Model):
    """ Stock model refers to a stock/share in a users account """
    StockStatuses = [('a', 'Active'), ('i', 'Inactive')]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user_profile = models.ForeignKey('dashboard.Profile', on_delete=models.CASCADE)
    ticker_data = models.ForeignKey('dashboard.Ticker', on_delete=models.PROTECT, null=True)
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
        """ Retrieve all trades for a given stock """
        trades = Trade.objects.filter(stock=self)
        if trades.count() > 0 and self.ticker_data:
            trades = trades.order_by('date')
        else:
            trades = None
        return trades

    def get_ticker(self):
        """ Convenience method to get ticker for given stock """
        return self.ticker

    def assign_ticker(self):
        """ Assign or create the relevant ticker object for a stock """
        if Ticker.objects.filter(ticker=self.get_ticker()).exists():
            self.ticker_data = Ticker.objects.get(ticker=self.get_ticker())
        else:
            Ticker.objects.new(ticker=self.get_ticker())

    def add_trade(self, trade):
        """ Function to update stock details when trade is added """
        if trade.trade_type == 'b':
            if len(self.trades()) > 1:
                self.quantity += trade.amount
                self.invested += trade.avg_price * trade.amount
                self.fees_usd += trade.fees_usd
            else:
                self.quantity = trade.amount
                self.invested = trade.avg_price * trade.amount
                self.fees_usd = trade.fees_usd
        else:
            if len(self.trades()) > 1:
                self.quantity -= trade.quantity
                self.fees_usd += trade.fees_usd
        self.save()