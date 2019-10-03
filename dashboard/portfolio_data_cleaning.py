""" Functions to clean and combine stock/trade data into portfolio chart json """
from datetime import datetime, date
from .historical_data import request_iex_charts_simple, request_chart_from_date
import pandas as pd
from .models import Stock, Trade, User, Profile, Portfolio

def find_all_portfolios():
	""" init portfolios if user has stocks """
	[PortfolioUpdate(user.profile) for user in User.objects.all() if user.profile.has_stocks()]


class PortfolioUpdate():
	""" Object for updating a users portfolio data """

	def __init__(self, profile):
		""" Initiate portfolio data for charting """
		self.portfolio = Portfolio.objects.update_or_create(user_profile=profile, name=profile.user.username, defaults={'data': "{}"})[0]
		self.stocks = Stock.objects.filter(user_profile=profile)
		self.benchmark = self.get_benchmark()
		""" Get the earliest trade date and retrieve benchmark data including that date """

		# For each stock combine trades and historical data if the stock has trades present
		stock_data = [self.combine_trades(stock) for stock in list(self.stocks) if stock.trades()]

	def get_benchmark(self):
		""" Get price chart for benchmark from earliest trade date """
		earliest_date = self.portfolio.earliest_trade().date
		time_diff = date.today() - earliest_date
		if int(time_diff.days/365) > 3:
			date_range = 'max'
		else:
			time_queries = {0: '6m', 1: '2y', 2: '5y', 3: '5y'}
			date_range = time_queries[int(time_diff.days/365)]
		day_chart = request_chart_from_date(date_range, self.portfolio.benchmark_ticker)
		return day_chart
	
	def combine_trades(self, stock):
		""" Combine trade data with historical prices to track performance """
		trade_list = list(stock.trades().values('date', 'amount', 'fees_usd', 'stock_id', 'trade_type', 'avg_price'))
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
		bench_data = pd.DataFrame.from_records(self.benchmark)
		pd.to_datetime(bench_data['date'])
		print(bench_data.loc[bench_data['date'] == date])
		day_chart = [day for day in self.benchmark if day['date'] == date]
		print(day_chart)
		avg_unadjusted = (day_chart[0]['uHigh'] + day_chart[0]['uLow'])/2
		print(avg_unadjusted)
		trade['benchmark_amount'] = trade['value']/avg_unadjusted
		return trade
