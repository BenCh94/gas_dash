from django.contrib import admin
from .models import Stock, Trade, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Stock)
admin.site.register(Trade)
