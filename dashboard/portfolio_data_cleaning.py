""" Functions to clean and combine stock/trade data into portfolio chart json """
from .historical_data import request_iex_charts_simple, request_chart_on_date
import pandas as pd
from .models import Stock, Trade, User, Profile, Portfolio

def find_all_portfolios():
	""" init portfolios if user has stocks """
	[init_portfolio(user.profile) for user in User.objects.all() if user.profile.has_stocks()]

def init_portfolio(profile):
	""" Initiate portfolio data for charting """
	portfolio = Portfolio.objects.update_or_create(user_profile=profile, name=profile.user.username, defaults={'data': "{}"})
	user_stocks = Stock.objects.filter(user_profile=profile)
	# For each stock combine trades and historical data if the stock has trades present
	stock_data = [combine_trades(stock, portfolio) for stock in list(user_stocks) if stock.trades()]

def combine_trades(stock, portfolio):
	""" Combine trade data with historical prices to track performance """
	trade_list = list(stock.trades().values('date', 'amount', 'fees_usd', 'stock_id', 'trade_type', 'avg_price'))
	for index, trade in enumerate(trade_list):
		if not index:
			trade['invested'] = (trade['amount']*trade['avg_price'])+trade['fees_usd']
			initial_trade = buy_benchmark(trade, portfolio)

def buy_benchmark(trade, portfolio):
	""" Buy an equivalent value of the portfolio benchmark on the day trade was executed """
	if portfolio[0].benchmark_ticker:
		date = trade['date']
		print(date)
		return trade
	else:
		trade['benchmark'] = 'None'
		return trade
