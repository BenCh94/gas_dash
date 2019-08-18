""" Functions to clean and combine stock/trade data into portfolio chart json """

import pandas as pd
from .models import Stock, Trade, User, Profile, Portfolio


def find_all_portfolios():
	""" init portfolios if user has stocks """
	[init_portfolio(user.profile) for user in User.objects.all() if user.profile.has_stocks()]

def init_portfolio(profile):
	""" Initiate portfolio data for charting """
	Portfolio.objects.update_or_create(user_profile=profile, name=profile.user.username, defaults={'data': "{}"})
	user_stocks = Stock.objects.filter(user_profile=profile)
	# This is where I left off need to implement code to actually update portfolios
