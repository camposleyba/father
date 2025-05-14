from django.contrib import admin
from .models import Expense, qBudget

class expenseAdmin(admin.ModelAdmin):
	list_display = ('title','quarter','rendido','is_active','created','expense_date')
	list_editable = ('is_active','expense_date')
	list_filter = ('quarter',)

admin.site.register(Expense, expenseAdmin)
admin.site.register(qBudget)
