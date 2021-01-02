""" Command to populate ticker table with company logos for active stocks """
import os
import json
import datetime
from django.db.utils import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from dashboard.services import IexCloudService
from dashboard.models import Ticker, Stock


class Command(BaseCommand):
    """ Pull logos from IEX """

    help = "Function retrieves logos for all active stocks"

    def handle(self, *args, **options):
        self.stdout.write('Finding active stocks...')
        active_stocks = Stock.objects.filter(status='a')
        tickers = ','.join(set([stock.ticker_data.ticker for stock in active_stocks]))
        logos = IexCloudService(os.environ.get('IEX_API')).logo_url(tickers)
        for stock in active_stocks:
            stock.ticker_data.logo_url = logos[stock.ticker_data.ticker]['logo']['url']
            stock.ticker_data.save()
        self.stdout.write(f'Updated logos for {len(active_stocks)} tickers')
