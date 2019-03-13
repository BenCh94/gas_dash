import datetime
import json
import ast
import statistics
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

class Portfolio(models.Model):
	user_profile = models.ForeignKey('dashboard.Profile', on_delete=models.CASCADE)
	data = JSONField()
	name = models.CharField(max_length=200)
	benchmark_name = models.CharField(max_length=200, null=True)
	benchmark_ticker = models.CharField(max_length=5, null=True)
	def __str__(self):
		return self.name

	def latest_day_data(self):
		data_str = ast.literal_eval(self.data)
		data = json.loads(data_str)
		days = len(data)
		latest = data[-1]
		latest['days'] = days
		gains = [d['pct_gain'] for d in data]
		bench_gains = [d['bench_gain_pct'] for d in data]
		latest['mean'] = statistics.mean(gains)
		latest['bench_mean'] = statistics.mean(bench_gains)
		latest['cv'] = statistics.stdev(gains)/statistics.mean(gains)
		latest['bench_cv'] = statistics.stdev(bench_gains)/statistics.mean(bench_gains)
		return latest

	class Meta:
		unique_together = ('user_profile', 'name')