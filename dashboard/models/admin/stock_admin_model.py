""" Admin console model for ticker objects """
from django.contrib import admin
from .. import Stock

class StockAdmin(admin.ModelAdmin):
    """ Admin site settings for stock model """
    list_display = ('name', 'user_profile', 'ticker_data')
