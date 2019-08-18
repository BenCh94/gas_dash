""" Functions used to retrieve and update historical data from the IEX cloud API """
import os
import requests as r
from .models import Stock, Ticker

# IEX_BASE_URL set in environemnt variables should use\
# sandbox unless in production version [beta, stable, v1 etc] to be set in env var

# By saving historical data in the ticker object the update function should only need to query most\
# recent close data to update. This will reduce message usage to a manageable level.

def update_ticker_data():
	""" Function to chain methods in update process """
	tickers = find_all_tickers()
	update_create_tickers(tickers)

def find_all_tickers():
	""" Function to retrieve all unique tickers in the system """
	tickers = list(set(Stock.objects.values_list('ticker', flat=True)))
	return tickers

def update_create_tickers(tickers):
	""" Function creates or updates tickers with chart data """
	ticker_objects = [Ticker.objects.update_or_create(ticker=ticker) for ticker in tickers]
	# Initiate new tickers, update_create returns True/False in tuple index 1 if new record created.
	new = [ticker_object[0].ticker for ticker_object in ticker_objects if ticker_object[1]]
	full_charts = request_iex_charts_simple('5y', ','.join(new))
	create_charts = [Ticker.objects.filter(ticker=ticker).update(historical_data=full_charts[ticker]) for ticker in full_charts.keys()]
	created = len(create_charts) - 1
	# Add to existing tickers
	existing = [ticker_object[0].ticker for ticker_object in ticker_objects if not ticker_object[1]]
	partial_charts = request_iex_charts_simple('5d', ','.join(existing))
	update_charts = [append_json(Ticker.objects.get(ticker=ticker), partial_charts[ticker]) for ticker in partial_charts.keys()]
	updated = len(update_charts)
	return f'Created: {created} new tickers, Updated: {updated} existing tickers'

def request_iex_charts_simple(date_range, tickers):
	""" Returns open, close, volume data for given time range and tickers """
	token = os.environ.get('IEX_API')
	base_url = os.environ.get('IEX_BASE_URL')
	query = f'/stock/market/batch?token={token}&symbols={tickers}&types=chart&range={date_range}&chartCloseOnly=true'
	url = base_url + query
	iex_req = r.get(url)
	return iex_req.json()

def append_json(ticker, chart_data):
	""" Function updates historical prices with one day of data """
	historical = ticker.historical_data
	last_day = chart_data['chart'][-1]
	latest_saved = historical['chart'][-1]
	if last_day['date'] != latest_saved['date']:
		historical['chart'].append(last_day)
		ticker.save()
