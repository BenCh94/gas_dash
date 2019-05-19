"""Functions used to retrieve and update historical data from the IEX cloud API"""

import pandas as pd
import requests as r
import datetime as dt
from .models import Stock

def find_all_tickers():
	""" Function to retrieve all unique tickers in the system """
	tickers = list(set(Stock.objects.values_list('ticker', flat=True)))
	return tickers

