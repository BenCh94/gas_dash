""" Function for the home dashboard """
from .stock_functions import get_current_value


def get_latest_data(portfolio, stocks):
	""" Get the last days data for stocks and portfolio """
	if portfolio:
		latest = portfolio.latest_day_data()
		current_value = get_current_value(stocks, latest)
		latest = {**latest, **current_value}
		return latest
	return ''
