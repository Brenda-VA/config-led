from django.db.models import Count, Prefetch, Q
from rest_framework import permissions, viewsets

from .models import ConfigurationProject, Controller, ProductFamily, ProductVariant
from .serializers import (
    ConfigurationProjectSerializer,
    ControllerSerializer,
    ProductFamilyDetailSerializer,
    ProductFamilyListSerializer,
    ProductVariantSerializer,
)


class ProductFamilyViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"

    def get_queryset(self):
        active_variants = ProductVariant.objects.filter(is_active=True).order_by(
            "display_order",
            "pixel_pitch",
        )
        return (
            ProductFamily.objects.filter(is_active=True)
            .annotate(variants_count=Count("variants", filter=Q(variants__is_active=True)))
            .prefetch_related(Prefetch("variants", queryset=active_variants))
            .order_by("display_order", "name")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductFamilyDetailSerializer
        return ProductFamilyListSerializer


class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        queryset = (
            ProductVariant.objects.filter(is_active=True, family__is_active=True)
            .select_related("family")
            .order_by("family__display_order", "family__name", "display_order", "pixel_pitch")
        )

        product_type = self.request.query_params.get("product_type")
        family_slug = self.request.query_params.get("family")

        if product_type:
            queryset = queryset.filter(family__product_type=product_type)
        if family_slug:
            queryset = queryset.filter(family__slug=family_slug)

        return queryset


class ControllerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ControllerSerializer

    def get_queryset(self):
        return Controller.objects.filter(is_active=True).order_by("display_order", "brand", "name")


class ConfigurationProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ConfigurationProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = (
            ConfigurationProject.objects.select_related(
                "selected_variant",
                "selected_variant__family",
                "controller",
                "user",
            )
            .all()
            .order_by("-updated_at", "-created_at")
        )

        user = self.request.user
        if user.is_staff or user.is_superuser:
            return queryset
        return queryset.filter(user=user)
