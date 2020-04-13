""" Command to set UUIDS for all objects """
from django.contrib.postgres.functions import RandomUUID
from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Ticker, Stock, Trade, Portfolio, Profile

class Command(BaseCommand):
    """ Pull symbols from iex and update or create ticker objects """
    help = "Function sets uuid in postgres db"

    def handle(self , *args, **options):
        self.stdout.write('Initialising UUID task')
        Ticker.objects.update(uuid=RandomUUID())
        self.stdout.write('Updated tickers')
        Stock.objects.update(uuid=RandomUUID())
        self.stdout.write('Updated stocks')
        Trade.objects.update(uuid=RandomUUID())
        self.stdout.write('Updated trades')
        Portfolio.objects.update(uuid=RandomUUID())
        self.stdout.write('Updated portfolios')
        Profile.objects.update(uuid=RandomUUID())
        self.stdout.write('Updated profiles')
