from django.shortcuts import get_object_or_404
from .models import Stock, Trade
from .iex_requests import batch_quotes
from .dash_functions import apply_trades

def recalculate(stock):
	stock_df = apply_trades(stock)
	stock.invested = stock_df['invested'].iloc[-1]
	stock.quantity = stock_df['amount'].iloc[-1]
	stock.fees_usd = stock_df['fees_usd'].iloc[-1]
	stock.save()

def get_current_quotes(stocks):
	tickers = ''
	for stock in stocks:
		tickers += (str(stock.get_ticker())).lower() + ','
	quotes = batch_quotes(tickers)
	for stock in stocks:
		stock.quote = quotes[stock.ticker]['quote']
	return stocks
	

