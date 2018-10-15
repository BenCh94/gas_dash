import datetime
import json
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class Portfolio(models.Model):
	user_profile = models.ForeignKey('dashboard.Profile', on_delete=models.CASCADE)
	benchmark = models.ForeignKey('dashboard.Benchmark', on_delete=models.SET_NULL, null=True)
	data = JSONField()
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

	def current_gain(self):
		port_array = json.loads(self.data)
		print(list(port_array))
		return port_array

	class Meta:
		unique_together = ('user_profile', 'name')