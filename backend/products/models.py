from django.db import models

class Product(models.Model):
    INDOOR = "indoor"
    OUTDOOR = "outdoor"

    TYPE_CHOICES = [
        (INDOOR, "Indoor"),
        (OUTDOOR, "Outdoor"),
    ]

    name = models.CharField(max_length=120)
    product_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    cabinet_width_mm = models.DecimalField(max_digits=8, decimal_places=2)
    cabinet_height_mm = models.DecimalField(max_digits=8, decimal_places=2)
    pixel_pitch = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name