from django.core.management.base import BaseCommand, CommandError
from dashboard.dash_functions import update_portfolio

class Command(BaseCommand):
	help = "function to drop db and seed with admin and my portfolio"

	def handle(self, *args, **options):
		self.stdout.write('seeding data...')
		try:
			update_portfolio()
		except ValueError:
			raise CommandError('Something went wrong')


def clear_data():
    """Deletes all the table data"""
    logger.info("Delete all tables")
    Benchmark.objects.all().delete()
    Portfolio.objects.all().delete()
    Stock.objects.all().delete()
    Trade.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.all().delete()
