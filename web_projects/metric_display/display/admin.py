from django.contrib import admin
from .models import metric, metricpivot, backlog, award, specification, validation

admin.site.register(metric)
admin.site.register(metricpivot)
admin.site.register(backlog)
admin.site.register(award)
admin.site.register(validation)
admin.site.register(specification)
