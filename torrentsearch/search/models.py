from django.db import models

class Search(models.Model):
	torrentSearch = models.CharField(max_length=100, blank=True)
	torrentList = models.JSONField(null=True)
	magnetlink = models.CharField(max_length=5000, blank=True)

	def __str__(self):
		return self.torrentSearch

class dropboxapitoken(models.Model):
	title = models.CharField(max_length=100, blank=True)
	appkey = models.CharField(max_length=100, blank=True)
	oauth2refreshtoken = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.title

