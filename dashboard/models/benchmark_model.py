from django.db import models

class Benchmark(models.Model):
	name = models.CharField(max_length=200)
	ticker = models.CharField(max_length=20)
	def __str__(self):
		return self.name
