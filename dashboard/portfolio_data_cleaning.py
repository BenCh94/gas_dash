""" Functions to clean and combine stock/trade data into portfolio chart json """
from .historical_data import request_iex_charts_simple, request_chart_on_date
import pandas as pd
from .models import Stock, Trade, User, Profile, Portfolio

def find_all_portfolios():
	""" init portfolios if user has stocks """
	[PortfolioUpdate(user.profile) for user in User.objects.all() if user.profile.has_stocks()]


class PortfolioUpdate():
	""" Object for updating a users portfolio data """

	def __init__(self, profile):
		""" Initiate portfolio data for charting """
		self.portfolio = Portfolio.objects.update_or_create(user_profile=profile, name=profile.user.username, defaults={'data': "{}"})
		self.stocks = Stock.objects.filter(user_profile=profile)
		# For each stock combine trades and historical data if the stock has trades present
		stock_data = [self.combine_trades(stock) for stock in list(self.stocks) if stock.trades()]

	def combine_trades(self, stock):
		""" Combine trade data with historical prices to track performance """
		trade_list = list(stock.trades().values('date', 'amount', 'fees_usd', 'stock_id', 'trade_type', 'avg_price'))
		if self.portfolio[0].benchmark_ticker:
			self.get_benchmarks(trade_list)

	def get_benchmarks(self, trade_list):
		""" Get the benchmark trade value onsmae day as trade """
		trade_data = []
		for index, trade in enumerate(trade_list):
			trade['value'] = trade['amount']*trade['avg_price']
			trade['invested'] = trade['value']+trade['fees_usd']
			if not index:
				initial_trade = self.buy_benchmark(trade)
			else:
				trade_data.append(self.buy_benchmark(trade))

	def buy_benchmark(self, trade):
		""" Buy an equivalent value of the portfolio benchmark on the day trade was executed """
		date = trade['date']
		day_chart = request_chart_on_date(date, self.portfolio[0].benchmark_ticker)
		avg_unadjusted = (day_chart[0]['uHigh'] + day_chart[0]['uLow'])/2
		trade['benchmark_amount'] = trade['value']/avg_unadjusted
		print(trade)
		return trade
