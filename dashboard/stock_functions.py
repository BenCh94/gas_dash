""" Function for dealing with Stock records """

from django.shortcuts import get_object_or_404
from .models import Stock, Trade, Ticker
from .iex_requests import batch_quotes

def get_current_quotes(stocks):
	""" Retrieves the latest quoted price for given list of stocks """
	tickers = ''
	for stock in stocks:
		tickers += (str(stock.get_ticker())).lower() + ','
	quotes = batch_quotes(tickers)
	for stock in stocks:
		stock.quote = quotes[stock.ticker]['quote']
	return stocks

def get_current_value(stocks, latest):
	""" Get todays difference when trading session is live """
	current_value = 0
	for stock in stocks:
		current_value += stock.quantity*stock.quote['latestPrice']
	day_diff = current_value - latest['value']
	day_pct = (day_diff/latest['value'])
	return {'day_change': day_diff, 'pct_change': day_pct}

def assign_ticker(stock):
	""" Assign or create the relevant ticker object for a stock """
	if Ticker.objects.filter(ticker=stock.get_ticker()).exists():
		stock.ticker_data = Ticker.objects.get(ticker=stock.get_ticker())
	else:
		Ticker.objects.new(ticker=stock.get_ticker())
		