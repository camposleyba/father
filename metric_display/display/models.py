from django.db import models

class metric(models.Model):
	manager = models.CharField(blank=True, max_length=200)
	developer = models.CharField(blank=True, max_length=200)
	bot_nbr = models.CharField(blank=True, max_length=200)
	tot_bots = models.IntegerField(default=0)
	tot_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

	def __str__(self):
		return self.bot_nbr

class metricpivot(models.Model):
	manager = models.CharField(blank=True, max_length=200)
	developer = models.CharField(blank=True, max_length=200)
	tot_bots = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
	tot_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

	def __str__(self):
		return self.manager

class backlog(models.Model):
	status = models.CharField(blank=True, max_length=200)
	bot_nbr = models.CharField(blank=True, max_length=200)
	title = models.CharField(blank=True, max_length=200)
	autotype = models.CharField(blank=True, max_length=200)
	region = models.CharField(blank=True, max_length=200)

	def __str__(self):
		return self.title