""" Functions used to retrieve and update historical data from the IEX cloud API """
import os
import datetime
from django.utils import timezone
import requests as r
import pandas as pd
from .models import Stock, Ticker

# IEX_BASE_URL set in environemnt variables should use\
# sandbox unless in production version [beta, stable, v1 etc] to be set in env var

# By saving historical data in the ticker object the update function should only need to query most\
# recent close data to update. This will reduce message usage to a manageable level.

def update_ticker_data():
	""" Function to chain methods in update process """
	tickers = find_all_tickers()
	print(update_create_tickers(tickers))

def hard_update_ticker_data():
	tickers = find_all_tickers()
	print(fill_tickers(tickers))

def find_all_tickers():
	""" Function to retrieve all unique tickers in the system """
	tickers = list(set(Stock.objects.values_list('ticker', flat=True)))
	return tickers

def fill_tickers(tickers):
	""" Function creates tickers with chart data """
	ticker_objects = [Ticker.objects.update_or_create(ticker=ticker) for ticker in tickers]
	# Initiate new tickers, update_create returns True/False in tuple index 1 if new record created.
	full_charts = request_iex_charts_simple('5y', ','.join([ticker_object[0].ticker for ticker_object in ticker_objects]))
	create_charts = [Ticker.objects.filter(ticker=ticker).update(historical_data=full_charts[ticker]) for ticker in full_charts.keys()]
	return f'Force Updated: {len(create_charts)-1} tickers'

def update_create_tickers(tickers):
	""" Function creates or updates tickers with chart data """
	ticker_objects = [Ticker.objects.update_or_create(ticker=ticker) for ticker in tickers]
	# Initiate new tickers, update_create returns True/False in tuple index 1 if new record created.
	new = [ticker_object[0].ticker for ticker_object in ticker_objects if ticker_object[1]]
	if new:
		full_charts = request_iex_charts_simple('5y', ','.join(new))
		create_charts = [Ticker.objects.filter(ticker=ticker).update(historical_data=full_charts[ticker]) for ticker in full_charts.keys()]
		created = len(create_charts) - 1
	else:
		created = 0
	# Add to existing tickers
	existing = [ticker_object[0].ticker for ticker_object in ticker_objects if check_updates(ticker_object)]
	if existing:
		partial_charts = request_iex_charts_simple('6m', ','.join(existing))
		update_charts = [append_json(Ticker.objects.get(ticker=ticker), partial_charts[ticker]) for ticker in partial_charts.keys()]
		updated = len(update_charts)
	else:
		updated = 0
	return f'Created: {created} new tickers, Updated: {updated} existing tickers'

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

def append_json(ticker, chart_data):
	""" Function updates historical prices with one day of data """
	historical = ticker.historical_data
	chart = pd.DataFrame(chart_data['chart'])
	chart['date'] = pd.to_datetime(chart['date'])
	latest_saved = historical['chart'][-1]
	update_date = pd.to_datetime(latest_saved['date'])
	updates = len(chart[chart['date'] > update_date])
	historical['chart'].extend(chart_data['chart'][-updates:])
	ticker.save()

def check_updates(ticker):
	""" Check last update of ticker and skip if within 24 hours """
	chart_data = pd.DataFrame(ticker[0].historical_data['chart'])
	chart_data['date'] = pd.to_datetime(chart_data['date'])
	return not ticker[1] and max(chart_data['date']) < datetime.datetime.today()
