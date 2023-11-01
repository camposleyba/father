from django.contrib import admin
from .models import Employee, mid_exchrate


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','band','pmr','salary_monthly')
    list_display_links = ('first_name','last_name',)


class mid_exchrateAdmin(admin.ModelAdmin):
    list_display = ('band','exch_rate','midpoint')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(mid_exchrate, mid_exchrateAdmin)
