from django.db import models


class Employee(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	designation = models.CharField(max_length=100)
	photo = models.ImageField(upload_to='images', blank=True)
	band = models.CharField(max_length=2)
	pmr = models.DecimalField(max_digits=5, decimal_places=2)
	salary_increase_ytd = models.DecimalField(max_digits=10, decimal_places=2)
	salary_monthly = models.DecimalField(max_digits=10, decimal_places=2)
	salary_usd = models.DecimalField(max_digits=10, decimal_places=2)
	title = models.CharField(max_length=100)


	def __str__(self):
		return self.last_name


class mid_exchrate(models.Model):
	band = models.CharField(max_length=2)
	midpoint = models.DecimalField(max_digits=10, decimal_places=2)
	exch_rate = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.band