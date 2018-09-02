from django.shortcuts import get_object_or_404
from .models import Stock, Trade
from .dash_functions import get_trade_data
from .iex_requests import batch_quotes


def recalc_stock(stock_id):
	stock = get_object_or_404(Stock, pk=stock_id)
	stock_df = get_trade_data(stock)
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
	

