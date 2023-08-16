from django.contrib import admin
from .models import votados, categorias


class votadosAdmin(admin.ModelAdmin):
	list_display = ('nombre','categoria','cuentavotos')

admin.site.register(votados, votadosAdmin)
admin.site.register(categorias)
