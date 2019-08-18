import pandas as pd 
import numpy as np
import json
import ast
import statistics
from datetime import datetime
from django.shortcuts import get_object_or_404
from .iex_requests import stock_price, batch_price
from .models import Stock, Trade, User, Profile, Portfolio
from .stock_functions import get_current_quotes, get_current_value, assign_ticker

def update_portfolio():
	users = User.objects.all()
	for user in users:
		if user.profile.has_stocks():
			portfolio = portfolio_data(Stock.objects.filter(user_profile=user.profile))
			print(user.username)
			Portfolio.objects.update_or_create(user_profile=user.profile, name=user.username, defaults={ 'data': portfolio })
			print('Done')

def portfolio_data(stocks):
	stock_dfs = []
	for stock in stocks:
		if stock.trades():
			trade_data = apply_trades(stock)
			stock_dfs.append(get_daily_data(trade_data, stock.get_ticker()))
	if len(stock_dfs) > 0:
		portfolio = combine_portfolio(pd.concat(stock_dfs))
		return json.dumps(portfolio)
	else:
		return "None"

def apply_trades(stock):
	trade_list = list(stock.trades().values('date', 'amount', 'fees_usd', 'stock_id', 'trade_type', 'avg_price'))
	trade_list[0]['invested'] = (trade_list[0]['amount']*trade_list[0]['avg_price'])+trade_list[0]['fees_usd']
	init_trade = buy_benchmark(trade_list[0])
	trade_df = pd.DataFrame(init_trade, index=[0])
	del trade_list[0]
	for trade in trade_list:
		trade['invested'] = (trade['amount']*trade['avg_price'])+trade['fees_usd']
		if trade['trade_type'] == 'b':
			trade_df = add_buy(trade, trade_df)
		else:
			trade_df = add_sell(trade, trade_df)
	stock.invested = trade_df['invested'].iloc[-1]
	stock.quantity = trade_df['amount'].iloc[-1]
	stock.fees_usd = trade_df['fees_usd'].iloc[-1]
	stock.save()
	return trade_df
	
def get_daily_data(df, ticker):
	price_chart = pd.DataFrame(stock_price(ticker))
	price_chart['date'] = pd.to_datetime(price_chart['date'])
	df['date'] = pd.to_datetime(df['date'])
	price_chart = price_chart[price_chart['date'] >= df['date'].iloc[0]]
	combined = combine_trades_price(df, price_chart)
	return combined
	
def add_buy(trade, df):
	last_entry = df.tail(1).to_dict(orient='records')
	trade['amount'] = trade['amount'] + last_entry[0]['amount']
	trade['fees_usd'] = trade['fees_usd'] + last_entry[0]['fees_usd']
	trade['invested'] = trade['invested'] + last_entry[0]['invested']
	trade = add_benchmark(trade, last_entry)
	df = df.append([trade], ignore_index=True)
	return df

def add_sell(trade, df):
	last_entry = df.tail(1).to_dict(orient='records')
	new_entry = trade
	new_entry['amount'] = trade['amount'] - last_entry[0]['amount']
	new_entry['fees_usd'] = trade['fees_usd'] + last_entry[0]['fees_usd']
	new_entry['invested'] =  (last_entry[0]['invested'] - trade['invested']) + trade['fees_usd']
	sell_benchmark(trade)
	df = df.append([new_entry], ignore_index=True)
	return df
	
def buy_benchmark(trade):
	stock = Stock.objects.get(pk=trade['stock_id'])
	portfolio = Portfolio.objects.filter(user_profile=stock.user_profile).first()
	benchmark = portfolio.benchmark_ticker
	if benchmark:
		# Get benchmark price on trade day
		buy_amount = trade['invested'] - trade['fees_usd']
		bench_chart = stock_price(benchmark)
		day = [day for day in bench_chart if day.get('date') == str(trade['date'])]
		# Average open/close and purchase amount
		price = (day[0]['open']+day[0]['close'])/2
		trade['bench_amnt'] = buy_amount/price
		trade['benchmark'] = benchmark
		return trade 
	else:
		trade['benchmark'] = 'None'
		return trade

def add_benchmark(trade, last_entry):
	if last_entry[0]['benchmark'] != 'None':
		buy_amount = trade['invested'] - trade['fees_usd']
		bench_chart = stock_price(last_entry[0]['benchmark'])
		day = [day for day in bench_chart if day.get('date') == str(trade['date'])]
		# Average open/close and purchase amount
		price = (day[0]['open']+day[0]['close'])/2
		trade['bench_amnt'] = buy_amount/price
		trade['benchmark'] = last_entry[0]['benchmark']
	trade['bench_amnt'] = trade['bench_amnt'] + last_entry[0]['bench_amnt']
	trade = buy_benchmark(trade)
	return trade

def sell_benchmark(trade):
	return 'none'

def combine_trades_price(trades, prices):
	"""Function applies trade dfs to price chart"""
	frames = []
	for index, row in trades.iterrows():
		if index < trades.index.max():
			end_date = trades['date'].iloc[index+1]
			mask = (prices['date'] >= row['date']) & (prices['date'] < end_date)
			price_df = prices.loc[mask]
			gain_df = apply_trade_data(price_df, row)
			gain_df = apply_benchmark(gain_df, row, end_date)
			frames.append(gain_df)
		else:
			price_df = prices[prices['date'] >= row['date']]
			gain_df = apply_trade_data(price_df, row)
			gain_df = apply_final_benchmark(gain_df, row)
			frames.append(gain_df)
	full_df = pd.concat(frames)
	return full_df

def apply_benchmark(df, trade, end_date):
	if trade['benchmark'] != 'None':
		bench_chart = pd.DataFrame(stock_price(str(trade['benchmark'])))
		bench_chart['date'] = pd.to_datetime(bench_chart['date'])
		mask = (bench_chart['date'] >= trade['date']) & (bench_chart['date'] < end_date)
		bench_prices = bench_chart.loc[mask]
		df['bench_value'] = bench_prices['close']*trade['bench_amnt']
		df['bench_gain'] = df['bench_value'] - df['invested']
		df['bench_gain_pct'] = (df['bench_gain']/df['invested'])*100
		return df
	else:
		return df
		
def apply_final_benchmark(df, trade):
	if trade['benchmark'] != 'None':
		bench_chart = pd.DataFrame(stock_price(str(trade['benchmark'])))
		bench_chart['date'] = pd.to_datetime(bench_chart['date'])
		bench_prices = bench_chart[bench_chart['date'] >= trade['date']]
		df['bench_value'] = bench_prices['close']*trade['bench_amnt']
		df['bench_gain'] = df['bench_value'] - df['invested']
		df['bench_gain_pct'] = (df['bench_gain']/df['invested'])*100
		return df
	else:
		return df

def apply_trade_data(df, trade):
	df['amount'] = trade['amount']
	df['fees_usd'] = trade['fees_usd']
	df['invested'] = trade['invested']
	df['value'] = df['close']*df['amount']
	df['gain'] = df['value'] - df['invested']
	df['gain_pct'] = (df['gain']/df['invested'])*100
	return df


def combine_portfolio(df):
	portfolio = df.groupby('date', as_index=False).agg({'gain': np.sum, 'value': np.sum, 'amount': np.sum, 'fees_usd': np.sum, 'invested': np.sum, 'bench_gain': np.sum })
	portfolio.apply(lambda x: x.to_json(orient='records'))
	portfolio_dict = portfolio.to_dict(orient='records')
	for d in portfolio_dict:
		d['date'] =  d['date'].strftime('%Y-%m-%d')
		d['pct_gain'] = (d['gain']/d['invested']) * 100
		d['bench_gain_pct'] = (d['bench_gain']/d['invested']) * 100
	return json.dumps(portfolio_dict)


def get_latest_data(portfolio, stocks):
	if portfolio:
		latest = portfolio.latest_day_data()
		current_value = get_current_value(stocks, latest)
		latest = {**latest, **current_value}
		return latest
	else:
		return ''
