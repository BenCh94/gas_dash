from django.contrib import admin
from .models import Stock, Trade, Profile, Portfolio

# Register your models here.
admin.site.register(Profile)
admin.site.register(Stock)
admin.site.register(Trade)
admin.site.register(Portfolio)
