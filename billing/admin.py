from django.contrib import admin
from .models import DailyStock, Product, Transaction

@admin.register(DailyStock)
class DailyStockAdmin(admin.ModelAdmin):
    list_display = ('date', 'kg_bought', 'cost_price_total', 'sale_price_per_kg')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'weight', 'total_price')
