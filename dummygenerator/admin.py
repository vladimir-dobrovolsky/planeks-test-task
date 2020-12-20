from django.contrib import admin

# Register your models here.
from .models import FakeCSVSchema, FakeCSVSchemaColumn


class ColumnsInline(admin.TabularInline):
    model = FakeCSVSchemaColumn
    extra = 0


class FakeCSVSchemaAdmin(admin.ModelAdmin):
    inlines = (ColumnsInline,)


admin.site.register(FakeCSVSchema, FakeCSVSchemaAdmin)
admin.site.register(FakeCSVSchemaColumn)
