from django.shortcuts import get_object_or_404
from .models import Stock, Trade
from .iex_requests import batch_quotes
from .dash_functions import apply_trades

def get_current_quotes(stocks):
	tickers = ''
	for stock in stocks:
		tickers += (str(stock.get_ticker())).lower() + ','
	quotes = batch_quotes(tickers)
	for stock in stocks:
		stock.quote = quotes[stock.ticker]['quote']
	return stocks
	

