from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import ConfigurationProject, Controller, ProductFamily, ProductVariant, UserProfile

#archivo para gestionar los datos desde el panel de admin, aqui se cargan al panel manualmente
class ProductVariantInline(admin.TabularInline):
    # Permite crear/editar variantes directamente dentro de la familia LED.
    model = ProductVariant
    extra = 0
    fields = [
        "model_name",
        "pixel_pitch",
        "brightness_nits",
        "cabinet_width_mm",
        "cabinet_height_mm",
        "cabinet_depth_mm",
        "refresh_rate_hz",
        "web_price_per_cabinet",
        "is_active",
        "display_order",
    ]
    ordering = ["display_order", "pixel_pitch"]


@admin.register(ProductFamily)
class ProductFamilyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "product_type",
        "is_active",
        "display_order",
        "updated_at",
    ]
    list_filter = ["product_type", "is_active"]
    search_fields = ["name", "slug", "subtitle", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["display_order", "name"]
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = [
        "model_name",
        "family",
        "pixel_pitch",
        "brightness_nits",
        "dimensions_label",
        "refresh_rate_hz",
        "web_price_per_cabinet",
        "is_active",
        "display_order",
    ]
    list_filter = ["family__product_type", "family", "is_active", "brightness_nits"]
    search_fields = ["model_name", "family__name"]
    ordering = ["family__display_order", "family__name", "display_order", "pixel_pitch"]
    autocomplete_fields = ["family"]


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display = ["name", "brand", "price", "is_active", "display_order"]
    list_filter = ["brand", "is_active"]
    search_fields = ["name", "brand"]
    ordering = ["display_order", "brand", "name"]


@admin.register(ConfigurationProject)
class ConfigurationProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "selected_variant",
        "columns",
        "rows",
        "calculated_area_m2",
        "calculated_total_pixels",
        "updated_at",
    ]
    list_filter = ["unit", "redundancy", "content_mode", "created_at", "updated_at"]
    search_fields = ["name", "user__username", "selected_variant__model_name"]
    ordering = ["-updated_at", "-created_at"]
    autocomplete_fields = ["user", "selected_variant", "controller"]
    readonly_fields = [
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
        "created_at",
        "updated_at",
    ]


class UserProfileInline(admin.StackedInline):
    # Muestra can_view_prices dentro del admin de User sin cambiar el modelo User.
    model = UserProfile
    can_delete = False
    extra = 0
    fields = ["can_view_prices", "company", "country", "phone"]


User = get_user_model()


class UserAdmin(DjangoUserAdmin):
    inlines = [UserProfileInline]


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)
