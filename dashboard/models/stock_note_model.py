""" Stock note model for storing notes attached to a stock """
import uuid
import datetime
from django.db import models
from django.contrib.postgres.functions import RandomUUID
from ckeditor.fields import RichTextField
from .stock_model import Stock

class StockNote(models.Model):
    """ User can store public/private notes for stocks """
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    stock = models.ForeignKey('dashboard.Stock', on_delete=models.CASCADE)
    public = models.BooleanField()
    title = models.CharField(max_length=200)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)
