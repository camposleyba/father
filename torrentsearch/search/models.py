from django.db import models

class Search(models.Model):
	torrentSearch = models.CharField(max_length=100, blank=True)
	torrentList = models.JSONField(null=True)

	def __str__(self):
		return self.torrentSearch
