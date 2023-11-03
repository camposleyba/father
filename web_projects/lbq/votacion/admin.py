from django.contrib import admin
from .models import votados, categorias


class votadosAdmin(admin.ModelAdmin):
	list_display = ('nombre','categoria','cuentavotos')
	search_fields = ('nombre','categoria',)

class categoriasAdmin(admin.ModelAdmin):
	list_display = ('categoria','ganador')
	search_fields = ('categoria',)

admin.site.register(votados, votadosAdmin)
admin.site.register(categorias, categoriasAdmin)
