""" Command to run updates on all stocks and portfolios daily """
from django.core.management.base import BaseCommand, CommandError
from dashboard.historical_data import update_ticker_data, update_benchmarks
from dashboard.services import PortfolioUpdate, TickerUpdateService
from dashboard.models import User

class Command(BaseCommand):
	""" Command code for update stocks/portfolios function """
	help = "function to update users portfolios"

	def handle(self, *args, **options):
		self.stdout.write('updating portfolios...')
		try:
			TickerUpdateService('tickers').update_tickers('update')
		except ValueError as e:
			raise CommandError(f'Something went wrong updating the ticker objects: {e}')

		# try:
		# 	update_benchmarks()
		# except ValueError as e:
		# 	raise CommandError(f'Something went wrong updating the benchmark ticker objects: {e}')

		# try:
		# 	portfolios = [PortfolioUpdate(user.profile).update() for user in User.objects.all() if user.profile.has_stocks()]
		# 	print(portfolios)
		# 	errors = portfolios.count('Error')
		# 	print(f'Updated: {len(portfolios) - errors}, Errors: {errors}')
		# except ValueError as e:
		# 	raise CommandError(f'Something went wrong cleaning portfolio data: {e}')
