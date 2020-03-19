""" Portfolio model for users overall holdings """
import json
import ast
import statistics
import datetime
import pandas as pd
from django.db import models
from django.contrib.postgres.fields import JSONField
from .trade_model import Trade
from .stock_model import Stock
from .ticker_model import Ticker
from ..iex_requests import batch_quotes

class Portfolio(models.Model):
    """ Portfolio model defintion for users overall holdings """
    user_profile = models.ForeignKey('dashboard.Profile', on_delete=models.CASCADE)
    data = JSONField(null=True)
    name = models.CharField(max_length=200)
    benchmark_name = models.CharField(max_length=200, default='Vanguard S&P 500')
    benchmark_ticker = models.CharField(max_length=5, null='voo')
    benchmark_data = JSONField(null=True)
    def __str__(self):
        return self.name

    def latest_day_data(self, quotes):
        """ Returns latest data for the given portfolio """
        """ WAY too long needs refactoring but functional for now """
        data = ast.literal_eval(self.data)
        if not data:
            return 'Empty portfolio response'
        else:
            portfolio_df = pd.DataFrame(data)
            portfolio_by_day = portfolio_df.groupby('date')
            latest_date = max(portfolio_df['date'])
            days = len(portfolio_by_day)
            latest_day = portfolio_by_day.get_group(latest_date)
            latest = dict()
            latest['date'] = datetime.datetime.fromtimestamp(int(latest_date)/1000).strftime('%Y-%m-%d')
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
            for stock in quotes:
                current_value += stock.quantity*stock.quote['latestPrice']
            latest['day_change'] = current_value - latest['value']
            latest['pct_change'] = (latest['day_change']/latest['value'])
            return latest

    def earliest_trade(self):
        """ Return the earliest trade in the portfolio """
        stocks = Stock.objects.filter(user_profile=self.user_profile)
        stock_ids = [stock.id for stock in stocks if stock.trades()]
        trades = Trade.objects.filter(stock_id__in=stock_ids)
        earliest = trades.order_by('date')[0]
        return earliest

    def get_current_quotes(self):
        """ Retrieves the latest quoted price for users list of stocks """
        stocks = Stock.objects.filter(user_profile=self.user_profile, status='a')
        tickers = ''
        for stock in stocks:
            tickers += (str(stock.get_ticker())).lower() + ','
        quotes = batch_quotes(tickers)
        for stock in stocks:
            stock.quote = quotes[stock.ticker]['quote']
        return stocks


    class Meta:
        unique_together = ('user_profile', 'name')
