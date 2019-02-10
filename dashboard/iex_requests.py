""" Requests to the IEX api """
import os
import json
import requests as r

iex_base_url = "https://api.iextrading.com/1.0"
iex_cloud_url = 'https://cloud.iexapis.com/beta'
auth_token = {'token': os.environ.get('IEX_API')}

def list_symbols():
	""" Function gets all available symbols from IEX API  """
	req = r.get(iex_cloud_url+"/ref-data/symbols", params=auth_token)
	symbols = req.json()
	symbol_list = [{'data':stock['symbol'], 'value':stock['name']} for stock in symbols]
	return symbol_list

def stock_price(ticker):
	""" Function gets share chart 5y"""
	req = r.get(iex_cloud_url+"/stock/"+ ticker +"/chart/5y?token="+os.environ.get('IEX_API'))
	prices = req.json()
	return prices

def get_stock_company(ticker):
	""" Function gets company details from IEX API """
	stock_comp = "/stock/" + ticker + "/company"
	ticker_comp = r.get(iex_base_url+stock_comp)
	comp = ticker_comp.json()
	return comp

def get_stock_logo(ticker):
	""" Function retrieves logo from IEX """
	stock_logo_url = "/stock/" + ticker + "/logo"
	ticker_logo = r.get(iex_base_url+stock_logo_url)
	logo = ticker_logo.json()
	return logo['url']


def stock_profile(ticker):
	""" Batch request for company details and logo url """
	batch_reqs = "/batch?types=company,logo,stats&range=5y"
	profile_req = r.get(iex_base_url+"/stock/"+ ticker + batch_reqs)
	profile_data = json.loads(profile_req.text)
	return profile_data

def batch_quotes(tickers):
	""" Batch request for most recent quotes """
	batch_reqs = "/stock/market/batch?symbols=" + tickers + "&types=quote&token=" + os.environ.get('IEX_API')
	quotes_req = r.get(iex_cloud_url + batch_reqs)
	quotes = quotes_req.json()
	return quotes

def batch_price(tickers):
	""" Batch request for most recent quotes """
	batch_reqs = "/stock/market/batch?symbols=" + tickers + "&types=chart&range=5y"
	quotes_req = r.get(iex_base_url + batch_reqs)
	quotes = quotes_req.json()
	return quotes
