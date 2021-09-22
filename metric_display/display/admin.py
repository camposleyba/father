from django.contrib import admin
from .models import metric, metricpivot

admin.site.register(metric)
admin.site.register(metricpivot)
