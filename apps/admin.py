from django.contrib import admin
from django.contrib.admin import register

from .models import Staff, Table, Menu

admin.site.register(Staff)
admin.site.register(Table)


@register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass
