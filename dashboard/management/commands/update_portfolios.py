from django.core.management.base import BaseCommand, CommandError
from dashboard.dash_functions import update_portfolio

class Command(BaseCommand):
	help = "function to update users portfolios"

	def handle(self, *args, **options):
		self.stdout.write('updating portfolios...')
		try:
			update_portfolio()
		except ValueError:
			raise CommandError('Something went wrong')
