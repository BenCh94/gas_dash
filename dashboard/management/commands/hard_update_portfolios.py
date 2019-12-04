""" Command to run updates on all stocks and portfolios daily """
from django.core.management.base import BaseCommand, CommandError
from dashboard.historical_data import hard_update_ticker_data
from dashboard.portfolio_data_cleaning import find_all_portfolios

class Command(BaseCommand):
	""" Command code for update stocks/portfolios function """
	help = "function to update users portfolios"

	def handle(self, *args, **options):
		self.stdout.write('updating portfolios...')
		try:
			hard_update_ticker_data()
		except ValueError:
			raise CommandError('Something went wrong updating the ticker objects...')

		try:
			find_all_portfolios()
		except ValueError:
			raise CommandError('Something went wrong cleaning portfolio data..')
