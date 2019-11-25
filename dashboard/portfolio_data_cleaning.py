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

def apply_trade_data(df, trade):
	df['amount'] = trade['amount']
	df['fees_usd'] = trade['fees_usd']
	df['invested'] = trade['invested']
	df['value'] = df['close']*df['amount']
	df['gain'] = df['value'] - df['invested']
	df['gain_pct'] = (df['gain']/df['invested'])*100
	return df

def apply_benchmark(df, bench_chart, trade, end_date):
	if end_date != '':
		bench_chart['date'] = pd.to_datetime(bench_chart['date'])
		mask = (bench_chart['date'] >= trade['date']) & (bench_chart['date'] < end_date)
		bench_prices = bench_chart.loc[mask]
		df['bench_value'] = bench_prices['close'].apply(lambda x: x*0.3)
		df['bench_gain'] = df['bench_value'] - df['invested']
		df['bench_gain_pct'] = (df['bench_gain']/df['invested'])*100
	else:
		bench_chart['date'] = pd.to_datetime(bench_chart['date'])
		bench_prices = bench_chart[bench_chart['date'] >= trade['date']]
		df['bench_value'] = bench_prices['close']*trade['benchmark_amount']
		df['bench_gain'] = df['bench_value'] - df['invested']
		df['bench_gain_pct'] = (df['bench_gain']/df['invested'])*100
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
		self.portfolio.benchmark_data = day_chart
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
		price_data['date'] = pd.to_datetime(price_data['date'])
		bench_chart = pd.DataFrame(self.portfolio.benchmark_data)
		bench_chart['date'] = pd.to_datetime(bench_chart['date'])
		frames = []
		for index, row in trade_df.iterrows():
			if index < trade_df.index.max():
				end_date = trade_df['date'].iloc[index+1]
				mask = (price_data['date'] >= row['date']) & (price_data['date'] < end_date)
				price_df = price_data.loc[mask]
				gain_df = apply_trade_data(price_df, row)
				gain_df = apply_benchmark(gain_df, bench_chart, row, end_date)
				frames.append(gain_df)
			else:
				price_df = price_data[price_data['date'] >= row['date']]
				gain_df = apply_trade_data(price_df, row)
				gain_df = apply_benchmark(gain_df, bench_chart, row, '')
				frames.append(gain_df)
		full_df = pd.concat(frames)
		print(full_df[['gain', 'gain_pct', 'value', 'bench_value', 'bench_gain', 'bench_gain_pct']])
		return full_df
