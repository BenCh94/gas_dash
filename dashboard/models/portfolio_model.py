import datetime

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class Portfolio(models.Model):
	user_profile = models.ForeignKey('dashboard.Profile', on_delete=models.CASCADE)
	data = JSONField()
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

	class Meta:
		unique_together = ('user_profile', 'name')