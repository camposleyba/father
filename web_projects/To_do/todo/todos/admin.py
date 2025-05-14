from django.contrib import admin
from .models import Todo


class todoAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)
	list_display = ('title','datecompleted','important','is_active',)
	search_fields = ('category','title',)
	list_editable = ('is_active','datecompleted','important')
	list_filter = ('category','important')

admin.site.register(Todo, todoAdmin)
