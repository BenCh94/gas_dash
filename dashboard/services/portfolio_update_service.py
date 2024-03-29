""" Service class to update portfolio json for charting """
import pandas as pd
import numpy as np
import json
import os
import logging
from datetime import date
from .iex_cloud_service import IexCloudService
from dashboard.models import Stock, User, Portfolio
from .stock_update_service import StockUpdate

class PortfolioUpdate():
	""" Class gathers all stocks and trades from a portfolio and updates historical data """
	def __init__(self, profile):
		""" Initiate portfolio data for charting """
		print(f'initialising portfolio update object {profile.user.username}...')
		self.portfolio = Portfolio.objects.update_or_create(user_profile=profile, name=profile.user.username)[0]
		self.stocks = Stock.objects.filter(user_profile=profile)
		""" Get the earliest trade date and retrieve benchmark data including that date """
		self.benchmark = self.portfolio.benchmark_object.historical_data

	def update(self):
		""" For each stock update using price charts if the stock has trades present """
		stock_data = [StockUpdate(self.benchmark, stock.ticker_data.historical_data, stock.trades()).get_update() for stock in list(self.stocks) if stock.trades()]
		print(f'got individual stock data {self.portfolio.name}')
		portfolio_data = pd.concat(stock_data)
		print(f'combined portfolio data {self.portfolio.name}')
		print(portfolio_data.sort_values(by='date'))
		self.portfolio.data = portfolio_data.to_json(orient='records')
		if len(portfolio_data) > 2:
			self.portfolio.save()
			return self.portfolio.name
		return 'Error'
