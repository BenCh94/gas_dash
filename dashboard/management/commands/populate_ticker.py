""" Command to populate ticker table with refrence data """
import os
import json
from django.core.management.base import BaseCommand, CommandError
from dashboard.services import IexCloudService
from dashboard.models import Ticker

class Command(BaseCommand):
    """ Pull symbols from iex and update or create ticker objects """
    help = "Function populates ticker table with reference data from IEX"

    def handle(self , *args, **options):
        self.stdout.write('Initialising ticker reference')
        try:
            symbols = IexCloudService(os.environ.get('IEX_API')).list_symbols()
        except ValueError as e:
            raise CommandError(f'Call to IEX failed: {e}')

        for symbol in json.load(symbols):
            print(symbol)