from django.conf import settings
from django.db import models
from django.utils.text import slugify


class ProductFamily(models.Model):
    # Modelo principal que el frontend muestra en el primer paso del configurador.
    # Sus imagenes son rutas/claves de assets locales de Nuxt, no ficheros subidos a Django.
    INDOOR = "indoor"
    OUTDOOR = "outdoor"

    PRODUCT_TYPE_CHOICES = [
        (INDOOR, "Indoor"),
        (OUTDOOR, "Outdoor"),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)
    subtitle = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    main_image = models.CharField(
        max_length=255,
        blank=True,
        help_text="Frontend asset key/path, for example leds/indoor/immersifPro.png.",
    )
    thumbnail_image = models.CharField(
        max_length=255,
        blank=True,
        help_text="Frontend asset key/path, for example leds/indoor/immersifPro.png.",
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "LED model family"
        verbose_name_plural = "LED model families"
        ordering = ["display_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    # Variante tecnica de una familia LED. El frontend usa estos datos para la tabla
    # de seleccion y para calcular medidas, resolucion, peso, potencia y calor.
    family = models.ForeignKey(
        ProductFamily,
        related_name="variants",
        on_delete=models.CASCADE,
    )
    model_name = models.CharField(max_length=160)
    pixel_pitch = models.DecimalField(max_digits=5, decimal_places=2)
    brightness_nits = models.PositiveIntegerField()
    cabinet_width_mm = models.DecimalField(max_digits=8, decimal_places=2)
    cabinet_height_mm = models.DecimalField(max_digits=8, decimal_places=2)
    cabinet_depth_mm = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    cabinet_weight_kg = models.DecimalField(max_digits=8, decimal_places=2)
    refresh_rate_hz = models.PositiveIntegerField()
    web_price_per_cabinet = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    resolution_width_px_per_cabinet = models.PositiveIntegerField()
    resolution_height_px_per_cabinet = models.PositiveIntegerField()
    max_power_w = models.DecimalField(max_digits=10, decimal_places=2)
    typical_power_w = models.DecimalField(max_digits=10, decimal_places=2)
    max_heat_btu_h = models.DecimalField(max_digits=10, decimal_places=2)
    typical_heat_btu_h = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "LED variant"
        verbose_name_plural = "LED variants"
        ordering = ["family__display_order", "family__name", "display_order", "pixel_pitch"]

    @property
    def dimensions_label(self):
        depth = f" x {self.cabinet_depth_mm:g}" if self.cabinet_depth_mm else ""
        return f"{self.cabinet_width_mm:g} x {self.cabinet_height_mm:g}{depth} mm"

    def __str__(self):
        return self.model_name


class Controller(models.Model):
    # Controladores disponibles para una configuracion. El precio se oculta por API si el usuario no tiene permiso para ver precios.
    NOVASTAR = "novastar"
    COLORLIGHT = "colorlight"
    OTHER = "other"

    BRAND_CHOICES = [
        (NOVASTAR, "Novastar"),
        (COLORLIGHT, "Colorlight"),
        (OTHER, "Other"),
    ]

    brand = models.CharField(max_length=40, choices=BRAND_CHOICES)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "brand", "name"]

    def __str__(self):
        return f"{self.get_brand_display()} {self.name}"


class ConfigurationProject(models.Model):
    # Configuracion guardada de un usuario: variante seleccionada + columnas/filas
    # + opciones. Los campos calculated_* se derivan de ProductVariant.
    METERS = "m"
    FEET = "ft"
    UNIT_CHOICES = [
        (METERS, "Meters"),
        (FEET, "Feet"),
    ]

    REDUNDANCY_NONE = "none"
    REDUNDANCY_POWER = "power"
    REDUNDANCY_DATA = "data"
    REDUNDANCY_CHOICES = [
        (REDUNDANCY_NONE, "No redundancy"),
        (REDUNDANCY_POWER, "Power"),
        (REDUNDANCY_DATA, "Data"),
    ]

    CONTENT_DEFAULT = "default_image"
    CONTENT_VIDEO = "preview_video"
    CONTENT_UPLOAD = "upload_image"
    CONTENT_NONE = "no_image"
    CONTENT_MODE_CHOICES = [
        (CONTENT_DEFAULT, "Default image"),
        (CONTENT_VIDEO, "Preview video"),
        (CONTENT_UPLOAD, "Upload image"),
        (CONTENT_NONE, "No image"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="configuration_projects",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=160)
    selected_variant = models.ForeignKey(
        ProductVariant,
        related_name="configuration_projects",
        on_delete=models.PROTECT,
    )
    controller = models.ForeignKey(
        Controller,
        related_name="configuration_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    wall_width_m = models.DecimalField(max_digits=8, decimal_places=2)
    wall_height_m = models.DecimalField(max_digits=8, decimal_places=2)
    columns = models.PositiveIntegerField()
    rows = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default=METERS)
    resolution_preset = models.CharField(max_length=20, blank=True)
    redundancy = models.CharField(
        max_length=20,
        choices=REDUNDANCY_CHOICES,
        default=REDUNDANCY_NONE,
    )
    content_mode = models.CharField(
        max_length=40,
        choices=CONTENT_MODE_CHOICES,
        default=CONTENT_DEFAULT,
    )
    custom_image_path = models.CharField(max_length=255, blank=True)
    calculated_width_m = models.DecimalField(max_digits=10, decimal_places=3)
    calculated_height_m = models.DecimalField(max_digits=10, decimal_places=3)
    calculated_area_m2 = models.DecimalField(max_digits=10, decimal_places=3)
    calculated_resolution_width = models.PositiveIntegerField()
    calculated_resolution_height = models.PositiveIntegerField()
    calculated_total_pixels = models.PositiveBigIntegerField()
    calculated_weight_kg = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_max_power_w = models.DecimalField(max_digits=12, decimal_places=2)
    calculated_typical_power_w = models.DecimalField(max_digits=12, decimal_places=2)
    calculated_max_heat_btu_h = models.DecimalField(max_digits=12, decimal_places=2)
    calculated_typical_heat_btu_h = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    @property
    def total_cabinets(self):
        return self.columns * self.rows

    def save(self, *args, **kwargs):
        # Mantiene los calculos sincronizados tambien si el proyecto se edita
        # desde admin, no solo cuando se crea por API.
        if self.selected_variant_id and self.columns and self.rows:
            from .services import calculate_project_metrics

            for field_name, value in calculate_project_metrics(
                self.selected_variant,
                self.columns,
                self.rows,
            ).items():
                setattr(self, field_name, value)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # Extension simple del User de Django para permisos de negocio.
    # Evita crear un CustomUser en esta fase inicial del proyecto.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="price_profile",
        on_delete=models.CASCADE,
    )
    can_view_prices = models.BooleanField(default=False)
    company = models.CharField(max_length=160, blank=True)
    country = models.CharField(max_length=80, blank=True)
    phone = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return f"{self.user} price permissions"
