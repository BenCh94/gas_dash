""" Requests to the coinapi.io api """
import os
import requests as r

class CoinApiService():
    """ Class for interactions with IEX cloud API """
    def __init__(self):
        """ Set credentials and URL """
        self.base_url = os.environ.get('COIN_API_BASE_URL')
        self.headers = {'X-CoinApi-Key': os.environ.get('COINAPI_KEY')}

    def list_symbols(self):
        """ Function gets all available symbols from coin API """
        req = r.get(f"{self.base_url}/symbols?filter_asset_id=ETH&filter_exchange_id=KRAKEN", headers=self.headers)
        symbols = req.json()
        symbol_list = [symbol for symbol in symbols]
        return symbol_list

    def symbol_historical(self, symbol_id):
        """ Function gets all available symbols from coin API """
        req = r.get(f"{self.base_url}/ohlcv/{symbol_id}/history?period_id=1DAY&time_start=2017-01-10", headers=self.headers)
        chart = req.json()
        return chart  

