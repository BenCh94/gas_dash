""" Functions to clean and combine stock/trade data into portfolio chart json """
from datetime import datetime, date
from .historical_data import request_iex_charts_simple, request_chart_from_date
import pandas as pd
from .models import Stock, Trade, User, Profile, Portfolio

def find_all_portfolios():
	""" init portfolios if user has stocks """
	[PortfolioUpdate(user.profile) for user in User.objects.all() if user.profile.has_stocks()]

def add_buy(trade, df):
	""" Add trade buy data to overall trade df """
	last_entry = df.tail(1).to_dict(orient='records')
	trade['amount'] = trade['amount'] + last_entry[0]['amount']
	trade['fees_usd'] = trade['fees_usd'] + last_entry[0]['fees_usd']
	trade['invested'] = trade['invested'] + last_entry[0]['invested']
	trade['benchmark_amount'] = trade['benchmark_amount'] + last_entry[0]['benchmark_amount']
	df = df.append([trade], ignore_index=True)
	return df

def add_sell(trade, df):
	""" Subtract trade sell data from overall trade df """
	last_entry = df.tail(1).to_dict(orient='records')
	trade['amount'] = last_entry[0]['amount'] - trade['amount']
	trade['fees_usd'] = trade['fees_usd'] + last_entry[0]['fees_usd']
	trade['invested'] = (last_entry[0]['invested'] - trade['invested']) + trade['fees_usd']
	trade['benchmark_amount'] = last_entry[0]['benchmark_amount'] - trade['benchmark_amount']
	df = df.append([trade], ignore_index=True)
	return df


class PortfolioUpdate():
	""" Object for updating a users portfolio data """

	def __init__(self, profile):
		""" Initiate portfolio data for charting """
		self.portfolio = Portfolio.objects.update_or_create(user_profile=profile, name=profile.user.username, defaults={'data': "{}"})[0]
		self.stocks = Stock.objects.filter(user_profile=profile)
		""" Get the earliest trade date and retrieve benchmark data including that date """
		self.benchmark = self.get_benchmark()

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
				initial_trade = self.calc_benchmark(trade)
			else:
				trade_data.append(self.calc_benchmark(trade))
		trade_df = pd.DataFrame(initial_trade, index=[0])
		for trade in trade_data:
			if trade['trade_type'] == 'b':
				trade_df = add_buy(trade, trade_df)
			else:
				trade_df = add_sell(trade, trade_df)
		return self.apply_historical_prices(trade_df, stock)

	def calc_benchmark(self, trade):
		""" Buy/Sell an equivalent value of the portfolio benchmark on the day trade was executed """
		bench_data = pd.DataFrame.from_records(self.benchmark)
		bench_data['date'] = pd.to_datetime(bench_data['date'])
		day_chart = bench_data.loc[bench_data['date'] == pd.Timestamp(trade['date'])]
		avg_unadjusted = (float(day_chart['uHigh']) + float(day_chart['uLow']))/2
		trade['benchmark_amount'] = trade['value']/avg_unadjusted
		return trade

	def apply_historical_prices(self, trade_df, stock):
		""" Apply trades to historical prices for performance data """
		price_data = pd.DataFrame(stock.ticker_data.historical_data['chart'])
		print(price_data)
		# NOW have trades and pricing data last step is combining the two into a unified dataframe showing performance over time.
