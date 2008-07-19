from django.contrib import admin
from basic.remarks.models import *


class BanAdmin(admin.ModelAdmin):
    list_display = ('rule', 'field')
    list_filter = ('field',)
    search_fields = ('rule',)

admin.site.register(Ban, BanAdmin)


class RemarkAdmin(admin.ModelAdmin):
    list_display = ('person_name', 'remark', 'submit_date', 'content_type', 'is_public')
    list_filter   = ('content_type',)
    search_fields = ('remark', 'person_name')
    ordering = ('-submit_date',)

admin.site.register(Remark, RemarkAdmin)