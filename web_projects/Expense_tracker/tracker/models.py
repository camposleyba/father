from django.db import models

class Expense(models.Model):

    quarter = models.CharField(max_length=2)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    expense_date = models.DateField(null=True,blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=00000000.00)
    rendido = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
    	return self.title

class qBudget(models.Model):
	quarter = models.CharField(max_length=2)
	budget = models.DecimalField(max_digits=10, decimal_places=2, default=00000000.00)
	tc = models.DecimalField(max_digits=10, decimal_places=2, default=00000000.00)

	def __str__(self):
		return self.quarter
