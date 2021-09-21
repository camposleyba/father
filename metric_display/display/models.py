from django.db import models

class metric(models.Model):
	manager = models.CharField(blank=True, max_length=200)
	developer = models.CharField(blank=True, max_length=200)
	bot_nbr = models.CharField(blank=True, max_length=200)
	tot_bots = models.IntegerField(default=0)
	tot_hours = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

	def __str__(self):
		return self.bot_nbr