from django.db import models


class Todo(models.Model):
	category = models.CharField(max_length=100, blank=True)
	title = models.CharField(max_length=100)
	memo = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	datecompleted = models.DateTimeField(null=True, blank=True)
	important = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)


	def __str__(self):
		return self.title
