""" Functions used to retrieve and update historical data from the IEX cloud API """
import os
import datetime
from django.utils import timezone
import requests as r
import pandas as pd
from .models import Stock, Ticker, Portfolio

# IEX_BASE_URL set in environemnt variables should use\
# sandbox unless in production version [beta, stable, v1 etc] to be set in env var

# By saving historical data in the ticker object the update function should only need to query most\
# recent close data to update. This will reduce message usage to a manageable level.

def update_ticker_data():
	""" Function to chain methods in update process """
	tickers = find_all_tickers()
	print(update_create_tickers(tickers))

def update_benchmarks():
	""" Function to chain methods in update process """
	tickers = find_all_benchmarks()
	print(update_create_tickers(tickers))

def hard_update_ticker_data():
	tickers = find_all_tickers()
	print(fill_tickers(tickers))

def find_all_tickers():
	""" Function to retrieve all unique tickers in the system """
	all_stocks = Stock.objects.all().prefetch_related('ticker_data')
	return [stock.ticker_data.ticker for stock in all_stocks]

def find_all_benchmarks():
	""" Function to retrieve all unique tickers in the system """
	all_portfolios = Portfolio.objects.all().prefetch_related('benchmark_object')
	return [portfolio.benchmark_object for portfolio in all_portfolios]

def fill_tickers(ticker_objects):
	""" Function creates tickers with chart data """
	# Initiate new tickers, update_create returns True/False in tuple index 1 if new record created.
	full_charts = request_iex_charts_simple('5y', ','.join([ticker_object.ticker for ticker_object in ticker_objects]))
	create_charts = [Ticker.objects.filter(ticker=ticker).update(historical_data=pd.DataFrame(full_charts[ticker]['chart']).to_json(orient='records')) for ticker in full_charts.keys()]
	return f'Force Updated: {len(create_charts)-1} tickers'

def update_create_tickers(ticker_objects):
	""" Function creates or updates tickers with chart data """
	# Initiate new tickers, update_create returns True/False in tuple index 1 if new record created.
	new = [ticker for ticker in ticker_objects if ticker.historical_data == None]
	print(new)
	# if new:
	# 	full_charts = request_iex_charts_simple('5y', ','.join(new))
	# 	create_charts = [Ticker.objects.filter(ticker=ticker).update(historical_data=full_charts[ticker]) for ticker in full_charts.keys()]
	# 	created = len(create_charts) - 1
	# else:
	# 	created = 0
	# # Add to existing tickers
	# existing = ticker_objects.filter(historical_data__isnull=False)
	# updates = [check_updates(ticker_object) for ticker_object in existing]
	# return f'Created: {created} new tickers, Updated: {len(existing)} existing tickers'

def request_iex_charts_simple(date_range, tickers):
	""" Returns open, close, volume data for given time range and tickers """
	token = os.environ.get('IEX_API')
	base_url = os.environ.get('IEX_BASE_URL')
	query = f'/stock/market/batch?token={token}&symbols={tickers}&types=chart&range={date_range}&chartCloseOnly=true'
	url = base_url + query
	iex_req = r.get(url)
	return iex_req.json()

def request_chart_from_date(date, ticker):
	""" Returns simple chart for the given date only """
	token = os.environ.get('IEX_API')
	base_url = os.environ.get('IEX_BASE_URL')
	query = f'/stock/{ticker}/chart/{date}?token={token}'
	url = base_url + query
	iex_req = r.get(url)
	return iex_req.json()

def append_json(ticker, chart_data, historical, latest_saved):
	""" Function updates historical prices with missing data """
	chart = pd.DataFrame(chart_data)
	chart['date'] = pd.to_datetime(chart['date'])
	chart.sort_values(by='date')
	updates_df = chart[chart['date'] > latest_saved]
	new_data = pd.concat([historical, updates_df])
	ticker.historical_data = new_data.to_json(orient='records')
	ticker.save()

def check_updates(ticker):
	""" Check last update of ticker and skip if within 24 hours """
	historical = pd.read_json(ticker.historical_data)
	historical['date'] = pd.to_datetime(historical['date'])
	historical.sort_values(by='date')
	latest_saved = historical.iloc[-1, historical.columns.get_loc("date")]
	if latest_saved < pd.to_datetime(datetime.datetime.today()):
		time_diff = pd.to_datetime(datetime.datetime.today()) - latest_saved
		days = int(time_diff.days)
		if days > 1:
			date_range = '5d'
		elif days > 4:
			date_range = '1m'
		elif days > 28:
			date_range = '3m'
		elif days > 90:
			date_range = '6m'
		elif days > 180:
			date_range = '1y'
		elif days > 364:
			date_range = '2y'
		elif days > 720:
			date_range = '5y'
		elif days > 1825:
			date_range = 'max'
		else:
			date_range = '5d'

		chart = request_chart_from_date(date_range, ticker.ticker)
		append_json(ticker, chart, historical, latest_saved)
		return 'Updated'
