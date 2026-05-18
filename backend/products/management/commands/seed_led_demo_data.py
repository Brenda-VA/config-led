from decimal import Decimal

from django.core.management.base import BaseCommand

from products.models import Controller, ProductFamily, ProductVariant

'''este archivo me enseña de donde salieron los datos iniciales como:
        - Inmersif pro
        - variantes
        - controladores                             '''
class Command(BaseCommand):
    help = "Load demo LED configurator data for local development."

    def handle(self, *args, **options):
        # Seed idempotente: update_or_create permite reejecutarlo sin duplicar registros.
        family, _ = ProductFamily.objects.update_or_create(
            slug="immersif-pro",
            defaults={
                "name": "Immersif Pro",
                "product_type": ProductFamily.INDOOR,
                "subtitle": "Fine pixel pitch COB indoor LED display",
                "description": "Demo data for the LED configurator. Technical values should be replaced with final datasheets before production use.",
                "main_image": "leds/indoor/immersifPro.png",
                "thumbnail_image": "leds/indoor/immersifPro.png",
                "is_active": True,
                "display_order": 10,
            },
        )

        variants = [
            {
                "model_name": "Immersif Pro COB 0.6",
                "pixel_pitch": Decimal("0.60"),
                "brightness_nits": 600,
                "refresh_rate_hz": 7680,
                "web_price_per_cabinet": Decimal("1820.00"),
                "cabinet_weight_kg": Decimal("7.20"),
                "max_power_w": Decimal("180.00"),
                "typical_power_w": Decimal("72.00"),
                "display_order": 10,
            },
            {
                "model_name": "Immersif Pro COB 0.7",
                "pixel_pitch": Decimal("0.70"),
                "brightness_nits": 600,
                "refresh_rate_hz": 7680,
                "web_price_per_cabinet": Decimal("1540.00"),
                "cabinet_weight_kg": Decimal("7.20"),
                "max_power_w": Decimal("175.00"),
                "typical_power_w": Decimal("70.00"),
                "display_order": 20,
            },
            {
                "model_name": "Immersif Pro COB 0.9",
                "pixel_pitch": Decimal("0.90"),
                "brightness_nits": 600,
                "refresh_rate_hz": 7680,
                "web_price_per_cabinet": Decimal("1180.00"),
                "cabinet_weight_kg": Decimal("7.00"),
                "max_power_w": Decimal("165.00"),
                "typical_power_w": Decimal("66.00"),
                "display_order": 30,
            },
            {
                "model_name": "Immersif Pro COB 1.2",
                "pixel_pitch": Decimal("1.20"),
                "brightness_nits": 1000,
                "refresh_rate_hz": 3840,
                "web_price_per_cabinet": Decimal("880.00"),
                "cabinet_weight_kg": Decimal("6.80"),
                "max_power_w": Decimal("150.00"),
                "typical_power_w": Decimal("60.00"),
                "display_order": 40,
            },
            {
                "model_name": "Immersif Pro COB 1.5",
                "pixel_pitch": Decimal("1.50"),
                "brightness_nits": 1000,
                "refresh_rate_hz": 3840,
                "web_price_per_cabinet": Decimal("720.00"),
                "cabinet_weight_kg": Decimal("6.80"),
                "max_power_w": Decimal("140.00"),
                "typical_power_w": Decimal("56.00"),
                "display_order": 50,
            },
            {
                "model_name": "Immersif Pro COB 1.8",
                "pixel_pitch": Decimal("1.80"),
                "brightness_nits": 1000,
                "refresh_rate_hz": 3840,
                "web_price_per_cabinet": Decimal("620.00"),
                "cabinet_weight_kg": Decimal("6.70"),
                "max_power_w": Decimal("132.00"),
                "typical_power_w": Decimal("52.80"),
                "display_order": 60,
            },
        ]

        for data in variants:
            pixel_pitch = data["pixel_pitch"]
            max_power = data["max_power_w"]
            typical_power = data["typical_power_w"]

            # Demo heat values use the common electrical conversion 1 W = 3.412 BTU/h.
            ProductVariant.objects.update_or_create(
                family=family,
                model_name=data["model_name"],
                defaults={
                    **data,
                    "cabinet_width_mm": Decimal("600.00"),
                    "cabinet_height_mm": Decimal("337.50"),
                    "cabinet_depth_mm": Decimal("42.00"),
                    "resolution_width_px_per_cabinet": round(Decimal("600.00") / pixel_pitch),
                    "resolution_height_px_per_cabinet": round(Decimal("337.50") / pixel_pitch),
                    "max_heat_btu_h": (max_power * Decimal("3.412")).quantize(Decimal("0.01")),
                    "typical_heat_btu_h": (typical_power * Decimal("3.412")).quantize(Decimal("0.01")),
                    "is_active": True,
                },
            )

        controllers = [
            {
                "brand": Controller.NOVASTAR,
                "name": "H2",
                "price": Decimal("980.00"),
                "display_order": 10,
            },
            {
                "brand": Controller.NOVASTAR,
                "name": "MX40 Pro",
                "price": Decimal("2450.00"),
                "display_order": 20,
            },
            {
                "brand": Controller.COLORLIGHT,
                "name": "X20",
                "price": Decimal("1320.00"),
                "display_order": 30,
            },
        ]

        for data in controllers:
            Controller.objects.update_or_create(
                brand=data["brand"],
                name=data["name"],
                defaults={**data, "is_active": True},
            )

        self.stdout.write(self.style.SUCCESS("Seeded LED demo data."))
