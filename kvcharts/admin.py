from django.contrib import admin
from .models import TiMethod, TiBenchResult


class TiMethodAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'id')


class TiBenchResultAdmin(admin.ModelAdmin):
    list_display = ('method', 'id', 'key_length', 'value_length', 'ts')


admin.site.register(TiMethod, TiMethodAdmin)
admin.site.register(TiBenchResult, TiBenchResultAdmin)
