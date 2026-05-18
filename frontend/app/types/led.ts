export type ProductType = "indoor" | "outdoor";
export type ConfigUnit = "meters" | "feet";
export type ResolutionMode = "FHD" | "UHD" | null;
export type RedundancyMode = "NO" | "POWER" | "DATA";
export type ContentMode = "default" | "preview" | "upload" | "none";
export type BackendUnit = "m" | "ft";
export type BackendRedundancyMode = "none" | "power" | "data";
export type BackendContentMode = "default_image" | "preview_video" | "upload_image" | "no_image";

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

export type LedController = {
  id: number;
  brand: string;
  name: string;
  price: string | null;
  is_active: boolean;
  display_order: number;
};

export type ConfiguratorState = {
  wallWidth: number;
  wallHeight: number;
  unit: ConfigUnit;
  columns: number;
  rows: number;
  resolutionMode: ResolutionMode;
  redundancy: RedundancyMode;
  contentMode: ContentMode;
  selectedModel: LedModel | null;
  selectedVariant: LedVariant | null;
  selectedController: LedController | null;
  controllerQuantity: number;
};

export type SaveProjectPayload = {
  name: string;
  selected_variant: number;
  controller?: number | null;
  wall_width_m: string;
  wall_height_m: string;
  columns: number;
  rows: number;
  unit: BackendUnit;
  resolution_preset: string;
  redundancy: BackendRedundancyMode;
  content_mode: BackendContentMode;
  custom_image_path?: string;
};

export type SavedProjectResponse = SaveProjectPayload & {
  id: number;
  selected_variant_detail: LedVariant;
  controller_detail: LedController | null;
  calculated_width_m: string;
  calculated_height_m: string;
  calculated_area_m2: string;
  calculated_resolution_width: number;
  calculated_resolution_height: number;
  calculated_total_pixels: number;
  calculated_weight_kg: string;
  calculated_max_power_w: string;
  calculated_typical_power_w: string;
  calculated_max_heat_btu_h: string;
  calculated_typical_heat_btu_h: string;
  total_cabinets: number;
  created_at: string;
  updated_at: string;
};
