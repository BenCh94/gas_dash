""" Command to populate ticker table with refrence data """
import os
import json
import datetime
from django.db.utils import IntegrityError
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

        for symbol in symbols:
            ticker = Ticker.create_from_iex(symbol)
            try:
                ticker.save()
                print(f"Successfully created ticker {ticker.ticker}")
            except IntegrityError as e:
                print('Violates constraints...')
                exsisting = Ticker.objects.filter(region=ticker.region, ticker=ticker.ticker)
                if exsisting.count() == 1:
                    if str(exsisting.first().reference_date) == ticker.reference_date:
                        print(f"Already up to date {ticker.ticker}")
                        continue
                    else:
                        exsisting.update(
                            name=ticker.name,
                            reference_date=ticker.reference_date,
                            active=ticker.active,
                            figi=ticker.figi,
                            cik=ticker.cik)
                        print(f"Updated: {ticker.ticker}")
                        continue
                elif exsisting.count() > 1:
                    exsisting = Ticker.objects.filter(provider_id=ticker.provider_id)
                    if exsisting.count() == 1:
                        exsisting.update(
                            name=ticker.name,
                            reference_date=ticker.reference_date,
                            active=ticker.active,
                            figi=ticker.figi,
                            cik=ticker.cik)
                        print(f"Updated: {ticker.ticker}")
                        continue
                    else:
                        print("Couldn't find exsisting record Error...")
                        continue
                else:
                    print(f'Unknown Error: ticker={ticker.ticker}, region={ticker.region}, name={ticker.name}')
                    continue
            except Exception as e:
                print(e)
                print(type(e))
                continue
