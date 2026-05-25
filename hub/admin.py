from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DataAnalyst, AnalysisDomain, Dataset, AnalysisProject


@admin.register(DataAnalyst)
class DataAnalystAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (("Additional Info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional Info", {"fields": ("position",)}),)
    )
    list_display = ["username", "email", "position", "is_staff"]

admin.site.register(AnalysisDomain)
admin.site.register(Dataset)
admin.site.register(AnalysisProject)
