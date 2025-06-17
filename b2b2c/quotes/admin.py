from django.contrib import admin

from .models import Branch, Product, Quote


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "branch", "base_price"]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ["product", "subscriber_name", "start_date", "duration", "price"]
