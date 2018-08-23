from django.shortcuts import get_object_or_404
from .models import Stock, Trade
from .dash_functions import get_trade_data


def recalc_stock(stock_id):
	stock = get_object_or_404(Stock, pk=stock_id)
	stock_df = get_trade_data(stock)
	stock.invested = stock_df['invested'].iloc[-1]
	stock.quantity = stock_df['amount'].iloc[-1]
	stock.fees_usd = stock_df['fees_usd'].iloc[-1]
	stock.save()
