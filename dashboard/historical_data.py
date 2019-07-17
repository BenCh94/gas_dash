"""Functions used to retrieve and update historical data from the IEX cloud API"""
import os
import pandas as pd
import requests as r
import datetime as dt
from .models import Stock, Ticker

# IEX_BASE_URL set in environemnt variables should use 
# sandbox unless in production version [beta, stable, v1 etc] to be set in env var

def update_portfolio_data():
	""" Function to chain methods in update process """
	tickers = find_all_tickers()
	data = request_iex_charts_simple('5y', ','.join(tickers))
	print(data)

def find_all_tickers():
	""" Function to retrieve all unique tickers in the system """
	tickers = list(set(Stock.objects.values_list('ticker', flat=True)))
	return tickers

def request_iex_charts_simple(date_range, tickers):
	""" Returns open, close, volume data for given time range and tickers """
	token = os.environ.get('IEX_API')
	base_url = os.environ.get('IEX_BASE_URL')
	query = f'/stock/market/batch?token={token}&symbols={tickers}&types=chart&range={date_range}&chartCloseOnly=true'
	url = base_url + query
	iex_req = r.get(url)
	return iex_req.json()

