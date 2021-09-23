from django.contrib import admin
from .models import metric, metricpivot, backlog

admin.site.register(metric)
admin.site.register(metricpivot)
admin.site.register(backlog)
