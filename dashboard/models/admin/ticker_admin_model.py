""" Admin console model for ticker objects """
from django.contrib import admin
from .. import Ticker

class TickerAdmin(admin.ModelAdmin):
    """ Admin site settings for ticker model """
    list_display = ('name', 'ticker', 'reference_date', 'created_at')
    search_fields = ('name', 'ticker')
