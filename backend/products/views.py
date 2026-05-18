#from django.shortcuts import render
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

'''ReadOnlyModelViewSet
↓
crea endpoints de lectura
↓
GET lista
↓
GET detalle'''
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).order_by("name")
    serializer_class = ProductSerializer