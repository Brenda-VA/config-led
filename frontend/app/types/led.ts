export type ProductType = "indoor" | "outdoor";

export type LedModel = {
  id: number;
  name: string;
  slug: string;
  product_type: ProductType;
  subtitle: string;
  description: string;
  main_image: string;
  thumbnail_image: string;
  variants_count: number;
  is_active: boolean;
  display_order: number;
};

export type LedVariant = {
  id: number;
  family: number;
  model_name: string;
  pixel_pitch: string;
  brightness_nits: number;
  cabinet_width_mm: string;
  cabinet_height_mm: string;
  cabinet_depth_mm: string | null;
  cabinet_weight_kg: string;
  refresh_rate_hz: number;
  web_price_per_cabinet: string | null;
  resolution_width_px_per_cabinet: number;
  resolution_height_px_per_cabinet: number;
  max_power_w: string;
  typical_power_w: string;
  max_heat_btu_h: string;
  typical_heat_btu_h: string;
  is_active: boolean;
  display_order: number;
};

export type LedModelDetail = LedModel & {
  variants: LedVariant[];
};
