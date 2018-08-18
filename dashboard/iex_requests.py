""" Requests to the IEX api """
import requests as r
import pandas as pd 
import json

iex_base_url = "https://api.iextrading.com/1.0/"

def list_symbols():
	req = r.get(iex_base_url+"ref-data/symbols") 
	symbols = req.json()
	symbol_list = [{'data':stock['symbol'], 'value':stock['name']} for stock in symbols]
	return symbol_list

def stock_price(ticker):
	""" Function gets share chart 5y"""
	req = r.get(iex_base_url+"stock/"+ ticker +"/chart/5y")
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
    profile_req = r.get(iex_base_url+"stock/"+ ticker + batch_reqs)
    profile_data = json.loads(profile_req.text)
    return profile_data
