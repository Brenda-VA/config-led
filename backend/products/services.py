from decimal import Decimal


MM_PER_METER = Decimal("1000")


def calculate_project_metrics(variant, columns, rows):
    """Calcula totales de pantalla a partir de datos de cabinet y columnas/filas."""
    columns = int(columns)
    rows = int(rows)
    total_cabinets = columns * rows

    width_m = (variant.cabinet_width_mm * columns) / MM_PER_METER
    height_m = (variant.cabinet_height_mm * rows) / MM_PER_METER
    area_m2 = width_m * height_m

    resolution_width = variant.resolution_width_px_per_cabinet * columns
    resolution_height = variant.resolution_height_px_per_cabinet * rows

    return {
        "calculated_width_m": width_m,
        "calculated_height_m": height_m,
        "calculated_area_m2": area_m2,
        "calculated_resolution_width": resolution_width,
        "calculated_resolution_height": resolution_height,
        "calculated_total_pixels": resolution_width * resolution_height,
        "calculated_weight_kg": variant.cabinet_weight_kg * total_cabinets,
        "calculated_max_power_w": variant.max_power_w * total_cabinets,
        "calculated_typical_power_w": variant.typical_power_w * total_cabinets,
        "calculated_max_heat_btu_h": variant.max_heat_btu_h * total_cabinets,
        "calculated_typical_heat_btu_h": variant.typical_heat_btu_h * total_cabinets,
    }


def user_can_view_prices(user):
    # Punto unico de decision para precios: los serializers lo consultan antes de devolver JSON.
    if not user or not user.is_authenticated:
        return False

    if user.is_staff or user.is_superuser:
        return True

    return bool(getattr(getattr(user, "price_profile", None), "can_view_prices", False))
