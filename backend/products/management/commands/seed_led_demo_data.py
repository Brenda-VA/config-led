from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from products.models import Controller, ProductFamily, ProductVariant


BTU_PER_WATT = Decimal("3.412")
DEMO_DESCRIPTION = (
    "Demo data for the LED configurator. Technical values should be replaced "
    "with final datasheets before production use."
)


class Command(BaseCommand):
    help = "Load demo LED configurator data for local development."

    def handle(self, *args, **options):
        managed_variant_names = {}

        for family_data in self.get_families():
            family = self.seed_family(family_data)
            managed_variant_names[family.id] = []

            for index, variant_data in enumerate(family_data["variants"], start=1):
                variant = self.seed_variant(family, variant_data, index * 10)
                managed_variant_names[family.id].append(variant.model_name)

        self.deactivate_removed_demo_variants(managed_variant_names)
        self.seed_controllers()

        self.stdout.write(self.style.SUCCESS("Seeded LED demo data."))

    def seed_family(self, family_data):
        self.warn_if_missing_asset(family_data["main_image"])

        family, _ = ProductFamily.objects.update_or_create(
            slug=family_data["slug"],
            defaults={
                "name": family_data["name"],
                "product_type": family_data["product_type"],
                "subtitle": family_data["subtitle"],
                "description": family_data.get("description", DEMO_DESCRIPTION),
                "main_image": family_data["main_image"],
                "thumbnail_image": family_data.get("thumbnail_image", family_data["main_image"]),
                "is_active": True,
                "display_order": family_data["display_order"],
            },
        )
        return family

    def seed_variant(self, family, variant_data, display_order):
        pixel_pitch = Decimal(str(variant_data["pixel_pitch"]))
        width = Decimal(str(variant_data["width_mm"]))
        height = Decimal(str(variant_data["height_mm"]))
        depth = Decimal(str(variant_data["depth_mm"]))
        max_power = Decimal(str(variant_data["max_power_w"]))
        typical_power = Decimal(str(variant_data["typical_power_w"]))

        variant, _ = ProductVariant.objects.update_or_create(
            family=family,
            model_name=variant_data["model_name"],
            defaults={
                "pixel_pitch": pixel_pitch,
                "brightness_nits": variant_data["brightness_nits"],
                "cabinet_width_mm": width,
                "cabinet_height_mm": height,
                "cabinet_depth_mm": depth,
                "cabinet_weight_kg": Decimal(str(variant_data["weight_kg"])),
                "refresh_rate_hz": variant_data["refresh_rate_hz"],
                "web_price_per_cabinet": Decimal(str(variant_data["price"])),
                "resolution_width_px_per_cabinet": round(width / pixel_pitch),
                "resolution_height_px_per_cabinet": round(height / pixel_pitch),
                # Demo heat values use the common electrical conversion 1 W = 3.412 BTU/h.
                "max_power_w": max_power,
                "typical_power_w": typical_power,
                "max_heat_btu_h": (max_power * BTU_PER_WATT).quantize(Decimal("0.01")),
                "typical_heat_btu_h": (typical_power * BTU_PER_WATT).quantize(Decimal("0.01")),
                "is_active": True,
                "display_order": display_order,
            },
        )
        return variant

    def deactivate_removed_demo_variants(self, managed_variant_names):
        for family_id, variant_names in managed_variant_names.items():
            ProductVariant.objects.filter(family_id=family_id).exclude(
                model_name__in=variant_names
            ).update(is_active=False)

    def warn_if_missing_asset(self, asset_path):
        asset_root = Path(settings.BASE_DIR).parent / "frontend" / "assets"
        if not (asset_root / asset_path).exists():
            self.stdout.write(self.style.WARNING(f"Missing frontend asset: {asset_path}"))

    def seed_controllers(self):
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

    def get_families(self):
        return [
            {
                "name": "Immersif Pro",
                "slug": "immersif-pro",
                "product_type": ProductFamily.INDOOR,
                "subtitle": "Immersif Pro Series - COB & SMD",
                "main_image": "leds/indoor/immersifPro.png",
                "display_order": 10,
                "variants": [
                    self.variant("Immersif Pro COB 0.6", "0.6", 600, 600, 337.5, 42, 7680, 1820, 7.2, 180, 72),
                    self.variant("Immersif Pro COB 0.7", "0.7", 600, 600, 337.5, 42, 7680, 1540, 7.2, 175, 70),
                    self.variant("Immersif Pro COB 0.9", "0.9", 600, 600, 337.5, 42, 7680, 1180, 7.0, 165, 66),
                    self.variant("Immersif Pro COB 1.2", "1.2", 1000, 600, 337.5, 42, 3840, 880, 6.8, 150, 60),
                    self.variant("Immersif Pro COB 1.5", "1.5", 1000, 600, 337.5, 42, 3840, 720, 6.8, 140, 56),
                    self.variant("Immersif Pro COB 1.8", "1.8", 1000, 600, 337.5, 42, 3840, 620, 6.7, 132, 52.8),
                ],
            },
            {
                "name": "Immersif Pro FC HB",
                "slug": "immersif-pro-fc-hb",
                "product_type": ProductFamily.INDOOR,
                "subtitle": "Immersif Pro Flipchip Series - SMD High Brightness",
                "main_image": "leds/indoor/ImmersifProFC.png",
                "display_order": 20,
                "variants": [
                    self.variant("Immersif Pro FC HB 1.2", "1.2", 3500, 600, 337.5, 42, 3840, 980, 7.6, 230, 92),
                    self.variant("Immersif Pro FC HB 1.5", "1.5", 3500, 600, 337.5, 42, 3840, 840, 7.5, 220, 88),
                    self.variant("Immersif Pro FC HB 1.8", "1.8", 3500, 600, 337.5, 42, 3840, 760, 7.5, 210, 84),
                    self.variant("Immersif Pro FC HB 2.5", "2.5", 3500, 600, 337.5, 42, 3840, 620, 7.4, 198, 79.2),
                    self.variant("Immersif Pro FC HB 3.7", "3.7", 3500, 600, 337.5, 42, 3840, 520, 7.4, 188, 75.2),
                ],
            },
            {
                "name": "Immersif",
                "slug": "immersif",
                "product_type": ProductFamily.INDOOR,
                "subtitle": "Immersif Series",
                "main_image": "leds/indoor/Immersif.png",
                "display_order": 30,
                "variants": [
                    self.variant("Immersif COB 0.7", "0.7", 600, 600, 337.5, 39, 3840, 1380, 6.9, 170, 68),
                    self.variant("Immersif COB 0.9", "0.9", 600, 600, 337.5, 39, 3840, 1080, 6.8, 160, 64),
                    self.variant("Immersif COB 1.2 600n", "1.2", 600, 600, 337.5, 39, 3840, 820, 6.6, 145, 58),
                    self.variant("Immersif COB 1.2 1000n", "1.2", 1000, 600, 337.5, 39, 7680, 900, 6.8, 168, 67.2),
                    self.variant("Immersif COB 1.5 600n", "1.5", 600, 600, 337.5, 39, 3840, 680, 6.5, 135, 54),
                    self.variant("Immersif COB 1.5 1000n", "1.5", 1000, 600, 337.5, 39, 7680, 740, 6.7, 156, 62.4),
                    self.variant("Immersif COB 1.8 600n", "1.8", 600, 600, 337.5, 39, 3840, 580, 6.5, 128, 51.2),
                    self.variant("Immersif COB 1.8 1000n", "1.8", 1000, 600, 337.5, 39, 7680, 640, 6.7, 148, 59.2),
                ],
            },
            {
                "name": "Reformer",
                "slug": "reformer",
                "product_type": ProductFamily.INDOOR,
                "subtitle": "Reformer Series - COB & SMD",
                "main_image": "leds/indoor/Reformer.png",
                "display_order": 40,
                "variants": [
                    self.variant("Reformer SMD 1.2", "1.2", 600, 640, 480, 64, 3840, 760, 8.8, 198, 79.2),
                    self.variant("Reformer SMD 1.5", "1.5", 600, 640, 480, 64, 3840, 680, 8.6, 188, 75.2),
                    self.variant("Reformer SMD 1.8", "1.8", 600, 640, 480, 64, 3840, 590, 8.4, 176, 70.4),
                    self.variant("Reformer SMD 2.5", "2.5", 700, 640, 480, 64, 3840, 480, 8.3, 168, 67.2),
                    self.variant("Reformer COB 1.5", "1.5", 600, 640, 480, 64, 3840, 720, 8.7, 190, 76),
                    self.variant("Reformer COB 1.8", "1.8", 600, 640, 480, 64, 3840, 620, 8.5, 180, 72),
                ],
            },
            {
                "name": "Rose",
                "slug": "rose",
                "product_type": ProductFamily.INDOOR,
                "subtitle": "Rose Series - SMD",
                "main_image": "leds/indoor/Rose.png",
                "display_order": 50,
                "variants": [
                    self.variant("Rose 0.9", "0.9", 600, 600, 337.5, 32, 3840, 1020, 5.6, 128, 51.2),
                    self.variant("Rose 1.2", "1.2", 600, 600, 337.5, 32, 3840, 760, 5.4, 120, 48),
                    self.variant("Rose 1.5", "1.5", 600, 600, 337.5, 32, 3840, 620, 5.2, 112, 44.8),
                    self.variant("Rose 1.8", "1.8", 800, 600, 337.5, 32, 3840, 540, 5.2, 118, 47.2),
                    self.variant("Rose 2.5", "2.5", 800, 600, 337.5, 32, 3840, 430, 5.0, 108, 43.2),
                ],
            },
            {
                "name": "Galax",
                "slug": "galax",
                "product_type": ProductFamily.OUTDOOR,
                "subtitle": "Galax Series - SMD",
                "main_image": "leds/outdoor/Galax.png",
                "display_order": 110,
                "variants": [
                    self.variant("Galax 2.9 1000x1000", "2.9", 5000, 1000, 1000, 83, 3840, 1280, 28, 650, 260),
                    self.variant("Galax 2.9 1000x500", "2.9", 5000, 1000, 500, 83, 3840, 780, 15, 330, 132),
                    self.variant("Galax 2.9 1500x1000", "2.9", 5000, 1500, 1000, 83, 3840, 1780, 42, 900, 360),
                    self.variant("Galax 2.9 1500x500", "2.9", 5000, 1500, 500, 83, 3840, 1160, 23, 500, 200),
                    self.variant("Galax 3.9 500x500", "3.9", 6000, 500, 500, 77.8, 3840, 420, 9, 180, 72),
                    self.variant("Galax 3.9 500x750", "3.9", 6000, 500, 750, 77.8, 3840, 560, 13, 260, 104),
                    self.variant("Galax 3.9 500x1000", "3.9", 6000, 500, 1000, 77.8, 3840, 680, 17, 340, 136),
                    self.variant("Galax 3.9 1000x1000", "3.9", 6000, 1000, 1000, 77.8, 3840, 1180, 28, 630, 252),
                    self.variant("Galax 3.9 1000x500", "3.9", 6000, 1000, 500, 83, 3840, 720, 15, 320, 128),
                    self.variant("Galax 3.9 1500x1000", "3.9", 6000, 1500, 1000, 83, 3840, 1680, 42, 880, 352),
                ],
            },
            {
                "name": "Galax HB",
                "slug": "galax-hb",
                "product_type": ProductFamily.OUTDOOR,
                "subtitle": "Galax Series - SMD High Brightness",
                "main_image": "leds/outdoor/GalaxHB.png",
                "display_order": 120,
                "variants": [
                    self.variant("Galax HB 5.7", "5.7", 10000, 960, 960, 80, 3840, 1320, 31, 950, 380),
                    self.variant("Galax HB 6.6", "6.6", 10000, 960, 960, 80, 3840, 1180, 31, 900, 360),
                    self.variant("Galax HB 8", "8", 10000, 960, 960, 80, 3840, 1020, 30, 850, 340),
                    self.variant("Galax HB 10", "10", 10000, 960, 960, 80, 3840, 880, 30, 800, 320),
                ],
            },
        ]

    def variant(
        self,
        model_name,
        pixel_pitch,
        brightness_nits,
        width_mm,
        height_mm,
        depth_mm,
        refresh_rate_hz,
        price,
        weight_kg,
        max_power_w,
        typical_power_w,
    ):
        return {
            "model_name": model_name,
            "pixel_pitch": pixel_pitch,
            "brightness_nits": brightness_nits,
            "width_mm": width_mm,
            "height_mm": height_mm,
            "depth_mm": depth_mm,
            "refresh_rate_hz": refresh_rate_hz,
            "price": price,
            "weight_kg": weight_kg,
            "max_power_w": max_power_w,
            "typical_power_w": typical_power_w,
        }
