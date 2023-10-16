from django.contrib import admin

from sales.models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("product", "date", "sales_number", "revenue", "user")
    list_filter = ("product", "user")
    search_fields = ("product",)
