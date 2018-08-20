import pandas as pd 

from .iex_requests import stock_price
from .models import Stock, Trade

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
	df = df.append([new_entry], ignore_index=True)
	return df

def get_trade_data(stock):
	trade_list = list(stock.trades().values('date', 'amount', 'fees_usd', 'stock_id', 'trade_type', 'avg_price'))
	init_data = pd.DataFrame([trade_list[0]])
	init_data['invested'] = (init_data['amount']*init_data['avg_price'])+init_data['fees_usd']
	del trade_list[0]
	for trade in trade_list:
		trade['invested'] = (trade['amount']*trade['avg_price'])+trade['fees_usd']
		if trade['trade_type'] == 'b':
			return add_buy(trade, init_data)
		else:
			return add_sell(trade, init_data)

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
	print(combined)



def portfolio_data(stocks):
	for stock in stocks:
		if stock.trades() == 'None':
			continue
		else:
			trade_data = get_trade_data(stock)
			stock_df = get_daily_data(trade_data, stock.get_ticker())