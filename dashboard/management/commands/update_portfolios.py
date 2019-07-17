from django.core.management.base import BaseCommand, CommandError
from dashboard.historical_data import update_portfolio_data

class Command(BaseCommand):
	help = "function to update users portfolios"

	def handle(self, *args, **options):
		self.stdout.write('updating portfolios...')
		try:
			update_portfolio_data()
		except ValueError:
			raise CommandError('Something went wrong')
