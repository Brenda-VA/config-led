from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "product_type",
        "cabinet_width_mm",
        "cabinet_height_mm",
        "pixel_pitch",
        "price",
        "is_active",
    ]
    list_filter = ["product_type", "is_active"]
    search_fields = ["name"]
