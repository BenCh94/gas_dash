from django.core.management.base import BaseCommand, CommandError
from dashboard.historical_data import find_all_tickers

class Command(BaseCommand):
	help = "function to update users portfolios"

	def handle(self, *args, **options):
		self.stdout.write('updating portfolios...')
		try:
			find_all_tickers()
		except ValueError:
			raise CommandError('Something went wrong')
