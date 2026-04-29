from django.db import models
from django.utils import timezone
from django.db.models import Sum

class DailyStock(models.Model):
    date = models.DateField(default=timezone.now)
    kg_bought = models.DecimalField(max_digits=10, decimal_places=3)
    cost_price_total = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    manual_profit_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Stock for {self.date}"

class Product(models.Model):
    name = models.CharField(max_length=255, default="Chicken")
    # In this specific app, we might only have one product "Chicken" 
    # but we'll keep the model for flexibility.
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    crate_wt = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    no_of_crates = models.IntegerField(default=1)
    birds_per_crate = models.IntegerField(default=0)
    remark = models.TextField(blank=True, null=True)
    group_no = models.CharField(max_length=50, blank=True, null=True)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.weight}kg at {self.timestamp}"
