from django.contrib import admin
from .models import Todo


class todoAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)
	list_display = ('category','title','created','datecompleted','important')
	search_fields = ('category','title',)

admin.site.register(Todo, todoAdmin)
