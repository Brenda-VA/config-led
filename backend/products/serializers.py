from rest_framework import serializers

from .models import ConfigurationProject, Controller, ProductFamily, ProductVariant
from .services import calculate_project_metrics, user_can_view_prices


class PriceProtectedSerializerMixin:
    # Este mixin se reutiliza en serializers con precios. Convierte el modelo a JSON
    # normalmente, pero sustituye los campos de precio por null si el request no tiene permiso.
    price_fields = ()

    def can_view_prices(self):
        request = self.context.get("request")
        return user_can_view_prices(getattr(request, "user", None))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not self.can_view_prices():
            for field_name in self.price_fields:
                if field_name in data:
                    data[field_name] = None
        return data


class ProductVariantSerializer(PriceProtectedSerializerMixin, serializers.ModelSerializer):
    # JSON de una variante LED. Incluye datos de su familia para que Nuxt no necesite
    # hacer otra peticion solo para saber el tipo indoor/outdoor o el slug del modelo.
    family_name = serializers.CharField(source="family.name", read_only=True)
    family_slug = serializers.CharField(source="family.slug", read_only=True)
    product_type = serializers.CharField(source="family.product_type", read_only=True)
    dimensions = serializers.CharField(source="dimensions_label", read_only=True)

    price_fields = ("web_price_per_cabinet",)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "family",
            "family_name",
            "family_slug",
            "product_type",
            "model_name",
            "pixel_pitch",
            "brightness_nits",
            "cabinet_width_mm",
            "cabinet_height_mm",
            "cabinet_depth_mm",
            "dimensions",
            "cabinet_weight_kg",
            "refresh_rate_hz",
            "web_price_per_cabinet",
            "resolution_width_px_per_cabinet",
            "resolution_height_px_per_cabinet",
            "max_power_w",
            "typical_power_w",
            "max_heat_btu_h",
            "typical_heat_btu_h",
            "is_active",
            "display_order",
        ]
        read_only_fields = ["id"]


class ProductFamilyListSerializer(serializers.ModelSerializer):
    # Respuesta ligera para /api/led-models/: suficiente para pintar tarjetas/listados.
    variants_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductFamily
        fields = [
            "id",
            "name",
            "slug",
            "product_type",
            "subtitle",
            "description",
            "main_image",
            "thumbnail_image",
            "variants_count",
            "is_active",
            "display_order",
        ]


class ProductFamilyDetailSerializer(ProductFamilyListSerializer):
    # Respuesta completa para /api/led-models/{slug}/: familia + variantes anidadas.
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta(ProductFamilyListSerializer.Meta):
        fields = ProductFamilyListSerializer.Meta.fields + ["variants"]


class ControllerSerializer(PriceProtectedSerializerMixin, serializers.ModelSerializer):
    # Los controladores tambien pasan por el mixin porque su precio es sensible.
    price_fields = ("price",)

    class Meta:
        model = Controller
        fields = [
            "id",
            "brand",
            "name",
            "price",
            "is_active",
            "display_order",
        ]


class ConfigurationProjectSerializer(serializers.ModelSerializer):
    # Serializer de lectura/escritura para proyectos guardados. El cliente envia
    # selected_variant, columnas y filas; Django rellena los calculated_*.
    selected_variant_detail = ProductVariantSerializer(source="selected_variant", read_only=True)
    controller_detail = ControllerSerializer(source="controller", read_only=True)
    total_cabinets = serializers.IntegerField(read_only=True)

    class Meta:
        model = ConfigurationProject
        fields = [
            "id",
            "name",
            "selected_variant",
            "selected_variant_detail",
            "controller",
            "controller_detail",
            "wall_width_m",
            "wall_height_m",
            "columns",
            "rows",
            "unit",
            "resolution_preset",
            "redundancy",
            "content_mode",
            "custom_image_path",
            "calculated_width_m",
            "calculated_height_m",
            "calculated_area_m2",
            "calculated_resolution_width",
            "calculated_resolution_height",
            "calculated_total_pixels",
            "calculated_weight_kg",
            "calculated_max_power_w",
            "calculated_typical_power_w",
            "calculated_max_heat_btu_h",
            "calculated_typical_heat_btu_h",
            "total_cabinets",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "calculated_width_m",
            "calculated_height_m",
            "calculated_area_m2",
            "calculated_resolution_width",
            "calculated_resolution_height",
            "calculated_total_pixels",
            "calculated_weight_kg",
            "calculated_max_power_w",
            "calculated_typical_power_w",
            "calculated_max_heat_btu_h",
            "calculated_typical_heat_btu_h",
            "total_cabinets",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        columns = attrs.get("columns", getattr(self.instance, "columns", None))
        rows = attrs.get("rows", getattr(self.instance, "rows", None))

        if columns is not None and columns < 1:
            raise serializers.ValidationError({"columns": "Columns must be at least 1."})
        if rows is not None and rows < 1:
            raise serializers.ValidationError({"rows": "Rows must be at least 1."})

        return attrs

    def create(self, validated_data):
        # El usuario no viene del JSON: viene de request.user porque el endpoint
        # de proyectos exige autenticacion.
        request = self.context.get("request")
        user = getattr(request, "user", None)

        validated_data["user"] = user
        validated_data.update(
            calculate_project_metrics(
                validated_data["selected_variant"],
                validated_data["columns"],
                validated_data["rows"],
            )
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Si cambian variante, columnas o filas, se recalculan los totales antes de guardar.
        selected_variant = validated_data.get("selected_variant", instance.selected_variant)
        columns = validated_data.get("columns", instance.columns)
        rows = validated_data.get("rows", instance.rows)

        validated_data.update(calculate_project_metrics(selected_variant, columns, rows))
        return super().update(instance, validated_data)
