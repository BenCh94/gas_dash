""" Requests to the IEX api """
import os
import json
import requests as r

token = os.environ.get('IEX_API')
base_url = os.environ.get('IEX_BASE_URL')

def list_symbols():
	""" Function gets all available symbols from IEX API """
	req = r.get(f"{base_url}/ref-data/symbols?token={token}")
	symbols = req.json()
	symbol_list = [{'data':stock['symbol'], 'value':stock['name']} for stock in symbols]
	return symbol_list

def stock_price(ticker):
	""" Function gets share chart 5y"""
	req = r.get(base_url+"/stock/"+ ticker +"/chart/5y")
	prices = req.json()
	return prices

def get_stock_company(ticker):
	""" Function gets company details from IEX API """
	stock_comp = "/stock/" + ticker + "/company"
	ticker_comp = r.get(base_url+stock_comp)
	comp = ticker_comp.json()
	return comp

def get_stock_logo(ticker):
	""" Function retrieves logo from IEX """
	stock_logo_url = "/stock/" + ticker + "/logo"
	ticker_logo = r.get(base_url+stock_logo_url)
	logo = ticker_logo.json()
	return logo['url']


def stock_profile(ticker):
	""" Batch request for company details and logo url """
	batch_reqs = f"{base_url}/stock/{ticker}/batch?token={token}&types=company,logo,stats&range=5y"
	profile_req = r.get(batch_reqs)
	profile_data = json.loads(profile_req.text)
	return profile_data


def batch_quotes(tickers):
	""" Batch request for most recent quotes """
	batch_reqs = f"{base_url}/stock/market/batch?token={token}&symbols={tickers}&types=quote"
	quotes_req = r.get(batch_reqs)
	quotes = quotes_req.json()
	return quotes

def batch_price(tickers):
	""" Batch request for most recent quotes """
	batch_reqs = f"{base_url}/stock/market/batch?token={token}&symbols={tickers}&types=chart&range=5y"
	quotes_req = r.get(batch_reqs)
	quotes = quotes_req.json()
	return quotes
