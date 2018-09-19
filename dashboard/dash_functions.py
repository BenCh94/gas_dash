import pandas as pd 
import numpy as np
import json
from datetime import datetime

from .iex_requests import stock_price
from .models import Stock, Trade, User, Profile, Portfolio

def add_buy(trade, df):
	last_entry = df.tail(1).to_dict(orient='records')
	trade['amount'] = trade['amount'] + last_entry[0]['amount']
	trade['fees_usd'] = trade['fees_usd'] + last_entry[0]['fees_usd']
	trade['invested'] = trade['invested'] + last_entry[0]['invested']
	df = df.append([trade], ignore_index=True)
	return df

def add_sell(trade, df):
	last_entry = df.tail(1).to_dict(orient='records')
	new_entry = trade
	new_entry['amount'] = trade['amount'] - last_entry[0]['amount']
	new_entry['fees_usd'] = trade['fees_usd'] + last_entry[0]['fees_usd']
	new_entry['invested'] =  (last_entry[0]['invested'] - trade['invested']) + trade['fees_usd']
	df = df.append([new_entry], ignore_index=True)
	return df

def get_trade_data(stock):
	trade_list = list(stock.trades().values('date', 'amount', 'fees_usd', 'stock_id', 'trade_type', 'avg_price'))
	trade_df = pd.DataFrame([trade_list[0]])
	trade_df['invested'] = (trade_df['amount']*trade_df['avg_price'])+trade_df['fees_usd']
	del trade_list[0]
	for trade in trade_list:
		trade['invested'] = (trade['amount']*trade['avg_price'])+trade['fees_usd']
		if trade['trade_type'] == 'b':
			trade_df = add_buy(trade, trade_df)
		else:
			trade_df = add_sell(trade, trade_df)
	return trade_df

def apply_trade_data(df, trade):
	df['amount'] = trade['amount']
	df['fees_usd'] = trade['fees_usd']
	df['invested'] = trade['invested']
	df['value'] = df['close']*df['amount']
	df['gain'] = df['value'] - df['invested']
	df['gain_pct'] = (df['gain']/df['invested'])*100
	return df


def combine_trades_price(trades, prices):
	frames = []
	for index, row in trades.iterrows():
		if index < trades.index.max():
			end_date = trades['date'].iloc[index+1]
			mask = (prices['date'] >= row['date']) & (prices['date'] < end_date)
			price_df = prices.loc[mask]
			gain_df = apply_trade_data(price_df, row)
			frames.append(gain_df)
		else:
			price_df = prices[prices['date'] >= row['date']]
			gain_df = apply_trade_data(price_df, row)
			frames.append(gain_df)
	full_df = pd.concat(frames)
	return full_df


def get_daily_data(df, ticker):
	price_chart = pd.DataFrame(stock_price(ticker))
	price_chart['date'] = pd.to_datetime(price_chart['date'])
	df['date'] = pd.to_datetime(df['date'])
	price_chart = price_chart[price_chart['date'] >= df['date'].iloc[0]]
	combined = combine_trades_price(df, price_chart)
	return combined


def combine_portfolio(df):
	portfolio = df.groupby('date', as_index=False).agg({'gain': np.sum, 'value': np.sum, 'amount': np.sum, 'fees_usd': np.sum, 'invested': np.sum })
	portfolio.apply(lambda x: x.to_json(orient='records'))
	portfolio_dict = portfolio.to_dict(orient='records')
	for d in portfolio_dict:
		d['date'] =  d['date'].strftime('%Y-%m-%d')
		d['pct_gain'] = (d['gain']/d['invested']) * 100
	return json.dumps(portfolio_dict)


def portfolio_data(stocks):
	stock_dfs = []
	for stock in stocks:
		if stock.trades():
			trade_data = get_trade_data(stock)
			stock_dfs.append(get_daily_data(trade_data, stock.get_ticker()))
	if len(stock_dfs) > 0:
		portfolio = combine_portfolio(pd.concat(stock_dfs))
		return json.dumps(portfolio)
	else:
		return "None"


def update_portfolio():
	users = User.objects.all()
	for user in users:
		if user.profile.has_stocks():
			portfolio = portfolio_data(Stock.objects.filter(user_profile=user.profile))
			print(portfolio)
			Portfolio.objects.update_or_create(user_profile=user.profile, name=user.username, defaults={ 'data': portfolio })

