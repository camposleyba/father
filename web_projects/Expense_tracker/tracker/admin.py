from django.contrib import admin
from .models import Expense, qBudget

class expenseAdmin(admin.ModelAdmin):
	readonly_fields = ('created',)

admin.site.register(Expense, expenseAdmin)
admin.site.register(qBudget)
