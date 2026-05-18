from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "product_type",
            "cabinet_width_mm",
            "cabinet_height_mm",
            "pixel_pitch",
            "price",
            "is_active",
        ]