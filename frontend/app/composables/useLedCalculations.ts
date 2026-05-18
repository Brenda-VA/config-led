import { computed, toValue, type MaybeRefOrGetter } from "vue";
import type { ConfigUnit, LedVariant } from "~/types/led";

type LedCalculationInput = {
  selectedVariant: MaybeRefOrGetter<LedVariant | null>;
  columns: MaybeRefOrGetter<number>;
  rows: MaybeRefOrGetter<number>;
  wallWidth?: MaybeRefOrGetter<number>;
  wallHeight?: MaybeRefOrGetter<number>;
  unit?: MaybeRefOrGetter<ConfigUnit>;
};

const METERS_PER_FOOT = 0.3048;
const FOUR_K_PIXELS = 8294400;

const toPositiveNumber = (value: unknown, fallback = 0) => {
  const parsedValue = Number(value);

  if (!Number.isFinite(parsedValue)) {
    return fallback;
  }

  return Math.max(parsedValue, 0);
};

const toPositiveInteger = (value: unknown, fallback = 1) => {
  return Math.max(1, Math.round(toPositiveNumber(value, fallback)));
};

const asMeters = (value: number, unit: ConfigUnit) => {
  return unit === "feet" ? value * METERS_PER_FOOT : value;
};

export const useLedCalculations = (input: LedCalculationInput) => {
  const selectedVariant = computed(() => toValue(input.selectedVariant));
  const columns = computed(() => toPositiveInteger(toValue(input.columns)));
  const rows = computed(() => toPositiveInteger(toValue(input.rows)));
  const unit = computed(() => toValue(input.unit) ?? "meters");

  const wallWidthM = computed(() => asMeters(toPositiveNumber(toValue(input.wallWidth)), unit.value));
  const wallHeightM = computed(() => asMeters(toPositiveNumber(toValue(input.wallHeight)), unit.value));

  const totalCabinets = computed(() => columns.value * rows.value);

  const cabinetWidthM = computed(() => {
    if (!selectedVariant.value) {
      return 0;
    }

    return toPositiveNumber(selectedVariant.value.cabinet_width_mm) / 1000;
  });

  const cabinetHeightM = computed(() => {
    if (!selectedVariant.value) {
      return 0;
    }

    return toPositiveNumber(selectedVariant.value.cabinet_height_mm) / 1000;
  });

  const displayWidthM = computed(() => cabinetWidthM.value * columns.value);
  const displayHeightM = computed(() => cabinetHeightM.value * rows.value);
  const displayAreaM2 = computed(() => displayWidthM.value * displayHeightM.value);

  const leftoverWidthM = computed(() => Math.max(wallWidthM.value - displayWidthM.value, 0));
  const leftoverHeightM = computed(() => Math.max(wallHeightM.value - displayHeightM.value, 0));
  const sideClearanceM = computed(() => leftoverWidthM.value / 2);
  const verticalClearanceM = computed(() => leftoverHeightM.value / 2);

  const diagonalInches = computed(() => {
    return Math.sqrt(displayWidthM.value ** 2 + displayHeightM.value ** 2) * 39.3701;
  });

  const totalWeightKg = computed(() => {
    if (!selectedVariant.value) {
      return 0;
    }

    return toPositiveNumber(selectedVariant.value.cabinet_weight_kg) * totalCabinets.value;
  });

  const resolutionWidth = computed(() => {
    return selectedVariant.value
      ? selectedVariant.value.resolution_width_px_per_cabinet * columns.value
      : 0;
  });

  const resolutionHeight = computed(() => {
    return selectedVariant.value
      ? selectedVariant.value.resolution_height_px_per_cabinet * rows.value
      : 0;
  });

  const totalPixels = computed(() => resolutionWidth.value * resolutionHeight.value);
  const controllers4k = computed(() => {
    return totalPixels.value > 0 ? Math.ceil(totalPixels.value / FOUR_K_PIXELS) : 0;
  });

  const maxPowerW = computed(() => {
    return selectedVariant.value
      ? toPositiveNumber(selectedVariant.value.max_power_w) * totalCabinets.value
      : 0;
  });

  const typicalPowerW = computed(() => {
    return selectedVariant.value
      ? toPositiveNumber(selectedVariant.value.typical_power_w) * totalCabinets.value
      : 0;
  });

  const maxHeatBtuH = computed(() => {
    return selectedVariant.value
      ? toPositiveNumber(selectedVariant.value.max_heat_btu_h) * totalCabinets.value
      : 0;
  });

  const typicalHeatBtuH = computed(() => {
    return selectedVariant.value
      ? toPositiveNumber(selectedVariant.value.typical_heat_btu_h) * totalCabinets.value
      : 0;
  });

  return {
    cabinetWidthM,
    cabinetHeightM,
    columns,
    rows,
    totalCabinets,
    wallWidthM,
    wallHeightM,
    displayWidthM,
    displayHeightM,
    displayAreaM2,
    sideClearanceM,
    verticalClearanceM,
    diagonalInches,
    totalWeightKg,
    resolutionWidth,
    resolutionHeight,
    totalPixels,
    controllers4k,
    maxPowerW,
    typicalPowerW,
    maxHeatBtuH,
    typicalHeatBtuH,
  };
};
