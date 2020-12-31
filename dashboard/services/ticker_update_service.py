""" Service class managing ticker object updates """
import os
import datetime
from django.utils import timezone
import requests as r
import pandas as pd
from .iex_cloud_service import IexCloudService
from dashboard.models import Stock, Ticker, Portfolio

class TickerUpdateService():
    """ Class for scheduled ticker updates methods """
    def __init__(self, update_type):
        """ all tickers to update """
        self.ticker_objects = self.__all_tickers() if (update_type == 'tickers') else self.__all_benchmarks()
        """ tickers with no historical data """
        self.new_tickers = [ticker for ticker in self.ticker_objects if ticker.historical_data == None]
        """ tickers with historical data """
        self.existing_tickers = [ticker for ticker in self.ticker_objects if not ticker.historical_data == None]

    def update_tickers(self, method):
        print(f'Updating {len(self.existing_tickers)} existing tickers')
        [self.__calculate_update(ticker_object) for ticker_object in self.existing_tickers]
        print(f'Populating {len(self.new_tickers)} new tickers')
        self.__populate_tickers(self.new_tickers)


    def __all_tickers(self):
        """ Function to retrieve all unique tickers associated with an active stock in the system """
        all_stocks = Stock.objects.filter(status='a').prefetch_related('ticker_data')
        return set([stock.ticker_data for stock in all_stocks])

    def __all_benchmarks(self):
        """ Function to retrieve all unique tickers in the system """
        all_portfolios = Portfolio.objects.filter(benchmark_object__is_null=False).prefetch_related('benchmark_object')
        return set([portfolio.benchmark_object for portfolio in all_portfolios])

    def __populate_tickers(self, fill_tickers):
        ticker_values = ','.join([ticker_object.ticker for ticker_object in fill_tickers])
        chart_data = IexCloudService(os.environ.get('IEX_API')).simple_chart(ticker_values, 'max')
        [Ticker.objects.filter(ticker=ticker).update(historical_data=pd.DataFrame(chart_data[ticker]['chart']).to_json(orient='records')) for ticker in chart_data.keys()]

    def __append_json(ticker_object, chart_data, historical, latest_saved):
        """ Function updates historical prices with missing data """
        chart = pd.DataFrame(chart_data)
        chart['date'] = pd.to_datetime(chart['date'])
        chart.sort_values(by='date')
        updates_df = chart[chart['date'] > latest_saved]
        new_data = pd.concat([historical, updates_df])
        ticker_object.historical_data = new_data.to_json(orient='records')
        ticker_object.save()

    def __calculate_update(self, ticker_object):
        """ Function to check the necessary data to update and request from IEX API """
        historical = pd.DataFrame(ticker_object.historical_data)
        historical['date'] = pd.to_datetime(historical['date'])
        historical.sort_values(by='date')
        latest_saved = historical.iloc[-1, historical.columns.get_loc("date")]
        if latest_saved < pd.to_datetime(datetime.datetime.today()):
            time_diff = pd.to_datetime(datetime.datetime.today()) - latest_saved
            days = int(time_diff.days)
            if days > 1:
                date_range = '5d'
            elif days > 4:
                date_range = '1m'
            elif days > 28:
                date_range = '3m'
            elif days > 90:
                date_range = '6m'
            elif days > 180:
                date_range = '1y'
            elif days > 364:
                date_range = '2y'
            elif days > 720:
                date_range = '5y'
            elif days > 1825:
                date_range = 'max'
            else:
                date_range = '5d'

            chart = IexCloudService(os.environ.get('IEX_API')).simple_chart(ticker_object.ticker, date_range)
            self.__append_json(ticker, chart, historical, latest_saved)
