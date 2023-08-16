from django.db import models

class votados(models.Model):
	nombre= models.CharField(max_length=100)
	apodo = models.CharField(max_length=100)
	categoria = models.CharField(max_length=100)
	foto = models.ImageField(upload_to='images', blank=True)
	cuentavotos = models.IntegerField(default=0)

	def __str__(self):
		return self.categoria+" "+self.nombre

class categorias(models.Model):
	categoria = models.CharField(max_length=100)

	def __str__(self):
		return self.categoria
