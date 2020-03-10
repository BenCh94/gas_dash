""" Function for the home dashboard """
from .stock_functions import get_current_value
import datetime


def get_latest_data(portfolio, stocks):
	""" Get the last days data for stocks and portfolio """
	if portfolio and portfolio.latest_day_data() != 'Empty portfolio response':
		latest = portfolio.latest_day_data()
		current_value = get_current_value(stocks, latest)
		latest = {**latest, **current_value}
		latest['date'] = datetime.datetime.fromtimestamp(int(latest['date'])/1000).strftime('%Y-%m-%d')
		return latest
	return 'Portfolio error, please refresh your data.'
