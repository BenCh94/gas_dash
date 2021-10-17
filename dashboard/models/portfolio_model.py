""" Portfolio model for users overall holdings """
import json
import ast
import statistics
import datetime
import uuid
import pandas as pd
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.postgres.functions import RandomUUID
from .trade_model import Trade
from .stock_model import Stock
from .ticker_model import Ticker
from .user_model import Profile
from ..iex_requests import batch_quotes

class Portfolio(models.Model):
    """ Portfolio model defintion for users overall holdings """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user_profile = models.ForeignKey('dashboard.Profile', on_delete=models.CASCADE)
    data = models.JSONField(null=True)
    name = models.CharField(max_length=200)
    benchmark_object = models.ForeignKey('dashboard.ticker', on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('user_profile', 'name')

    def latest_day_data(self, quotes):
        """ Returns latest data for the given portfolio """
        """ WAY too long needs refactoring but functional for now """
        if not self.data:
            return 'Empty portfolio response'
        data = ast.literal_eval(self.data)
        portfolio_df = pd.DataFrame(data)
        portfolio_by_day = portfolio_df.groupby('date')
        latest_date = max(portfolio_df['date'])
        days = len(portfolio_by_day)
        latest_day = portfolio_by_day.get_group(latest_date)
        latest = dict()
        date_object = datetime.datetime.fromtimestamp(int(latest_date)/1000)
        latest['date'] = date_object.strftime('%Y-%m-%d')
        latest['days'] = days
        latest['value'] = sum(latest_day['value'])
        latest['gain'] = sum(latest_day['gain'])
        latest['bench_gain'] = sum(latest_day['bench_gain'])
        latest['gain_pct'] = (sum(latest_day['gain'])/sum(latest_day['invested']))*100
        latest['bench_gain_pct'] = (sum(latest_day['bench_gain'])/sum(latest_day['invested']))*100
        latest['bench_gain'] = sum(latest_day['bench_gain'])
        latest['mean'] = statistics.mean(portfolio_df['gain_pct'])
        latest['bench_mean'] = statistics.mean(portfolio_df['bench_gain_pct'])
        latest['cv'] = statistics.stdev(portfolio_df['gain_pct'])/statistics.mean(portfolio_df['gain_pct'])
        latest['bench_cv'] = statistics.stdev(portfolio_df['bench_gain_pct'])/statistics.mean(portfolio_df['bench_gain_pct'])
        current_value = 0
        active_stocks = [stock for stock in quotes if stock.trades()]
        for stock in active_stocks:
            current_value += stock.quantity*stock.quote['latestPrice']
        if stock.quote['isUSMarketOpen']:
            latest['marketOpen'] = True
            latest['day_change'] = current_value - latest['value']
            latest['pct_change'] = (latest['day_change']/latest['value'])
        else:
            latest['marketOpen'] = False
            second_last_day = date_object - datetime.timedelta(days=1)
            group_label = int(datetime.datetime.timestamp(second_last_day))*1000
            if group_label in portfolio_by_day.groups:
                second_day = portfolio_by_day.get_group(group_label)
                latest['day_change'] = latest['value'] - sum(second_day['value'])
                latest['pct_change'] = (latest['day_change']/sum(second_day['value']))
            else:
                latest['day_change'] = 0
                latest['pct_change'] = 0   
        return latest

    def earliest_trade(self):
        """ Return the earliest trade in the portfolio """
        stocks = Stock.objects.filter(user_profile=self.user_profile, status='a')
        stock_ids = [stock.id for stock in stocks if stock.trades()]
        trades = Trade.objects.filter(stock_id__in=stock_ids)
        earliest = trades.order_by('date')[0]
        return earliest

    def get_current_quotes(self, status):
        """ Retrieves the latest quoted price for users list of stocks """
        stocks = Stock.objects.filter(user_profile=self.user_profile, status=status)
        tickers = ''
        for stock in stocks:
            tickers += (str(stock.get_ticker())).lower() + ','
        quotes = batch_quotes(tickers)
        for stock in stocks:
            stock.quote = quotes[stock.ticker]['quote']
            stock.held = stock.days_held()
        return stocks

@receiver(post_save, sender=Profile)
def create_user_portfolio(sender, instance, created, **kwargs):
    # profile creation skipped in testing env to allow manual creation in fixtures
    if created and not kwargs.get('raw', False):
        Portfolio.objects.create(user_profile=instance)

