from django.db import models

class Award(models.Model):
    
    quarter = models.CharField(max_length=2)
    award_category = models.CharField(max_length=100)
    who = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    monto = models.DecimalField(max_digits=7, decimal_places=2, default=00000.00)
    bp = models.BooleanField(default=False)
    
    def __str__(self):
    	return self.award_category
