""" Requests to the IEX api """
import os
import requests as r

class IexCloudService():
    """ Class for interactions with IEX cloud API """
    def __init__(self, token):
        """ Set credentials and URL """
        self.token = token
        self.base_url = os.environ.get('IEX_BASE_URL')

    def list_symbols(self):
        """ Function gets all available symbols from IEX API """
        req = r.get(f"{self.base_url}/ref-data/symbols?token={self.token}")
        symbols = req.json()
        symbol_list = [stock for stock in symbols]
        return symbol_list

    def batch_quotes(self, tickers):
        """ Batch request for most recent quotes """
        batch_reqs = f"{self.base_url}/stock/market/batch?token={self.token}&symbols={tickers}&types=quote"
        quotes_req = r.get(batch_reqs)
        quotes = quotes_req.json()
        return quotes

    def chart_from_date(self, ticker, date):
        query = f'{self.base_url}/stock/{ticker}/chart/{date}?token={self.token}'
        iex_req = r.get(query)
        return iex_req.json()


    def simple_chart(self, tickers, date_range):
        """ Function returns simplified chart data for given range """
        query = f'{self.base_url}/stock/market/batch?token={self.token}&symbols={tickers}&types=chart&range={date_range}&chartCloseOnly=true'
        iex_req = r.get(query)
        return iex_req.json()
