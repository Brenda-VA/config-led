<script setup lang="ts">
import type { LedVariant, RedundancyMode } from "~/types/led";

const props = defineProps<{
  selectedVariant: LedVariant | null;
  columns: number;
  rows: number;
  redundancy: RedundancyMode;
}>();

const calculations = useLedCalculations({
  selectedVariant: toRef(props, "selectedVariant"),
  columns: toRef(props, "columns"),
  rows: toRef(props, "rows"),
});

const formatNumber = (value: number, digits = 0) => {
  if (!props.selectedVariant) {
    return "-";
  }

  return value.toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
};

const formatUnitValue = (value: number, unit: string, digits = 0) => {
  if (!props.selectedVariant) {
    return "-";
  }

  return `${formatNumber(value, digits)} ${unit}`;
};

const formatMeters = (value: number) => formatUnitValue(value, "m", 2);
const formatArea = (value: number) => formatUnitValue(value, "m2", 2);
const formatWeight = (value: number) => formatUnitValue(value, "kg", 1);
const formatPower = (value: number) => formatUnitValue(value, "W");
const formatHeat = (value: number) => formatUnitValue(value, "BTU/h");
</script>

<template>
  <div class="grid grid-cols-1 gap-5 lg:grid-cols-[minmax(0,1fr)_360px]">
    <section class="rounded-2xl bg-white p-6 shadow-sm">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 class="text-2xl font-black tracking-normal">Structural Components</h2>
          <p class="mt-1 text-sm text-neutral-500">Base prepared for back frames and strips.</p>
        </div>

        <div class="flex gap-3">
          <button type="button" class="h-10 rounded border border-neutral-300 px-4 text-sm font-semibold">
            Add Back Frames
          </button>
          <button type="button" class="h-10 rounded border border-neutral-300 px-4 text-sm font-semibold">
            Add Strips
          </button>
        </div>
      </div>
    </section>

    <section class="rounded-2xl bg-white p-6 shadow-sm">
      <h2 class="text-2xl font-black tracking-normal">Specifications</h2>

      <dl class="mt-5 space-y-3 text-sm">
        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Screen Configuration</dt>
          <dd class="font-semibold">
            {{ selectedVariant ? `${calculations.columns.value} x ${calculations.rows.value}` : "-" }}
          </dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">No. of Cabinets</dt>
          <dd class="font-semibold">
            {{ selectedVariant ? calculations.totalCabinets.value : "-" }}
          </dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Dimensions</dt>
          <dd class="font-semibold">
            <template v-if="selectedVariant">
              {{ formatMeters(calculations.displayWidthM.value) }} x
              {{ formatMeters(calculations.displayHeightM.value) }}
            </template>
            <template v-else>-</template>
          </dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Display Area</dt>
          <dd class="font-semibold">{{ formatArea(calculations.displayAreaM2.value) }}</dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Diagonal</dt>
          <dd class="font-semibold">
            {{ selectedVariant ? `${formatNumber(calculations.diagonalInches.value, 1)} in` : "-" }}
          </dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Weight</dt>
          <dd class="font-semibold">{{ formatWeight(calculations.totalWeightKg.value) }}</dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Resolution</dt>
          <dd class="font-semibold">
            <template v-if="selectedVariant">
              {{ calculations.resolutionWidth.value }} x {{ calculations.resolutionHeight.value }}
            </template>
            <template v-else>-</template>
          </dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Total pixel quantity</dt>
          <dd class="font-semibold">{{ formatNumber(calculations.totalPixels.value) }}</dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Redundancy</dt>
          <dd class="font-semibold">{{ selectedVariant ? redundancy : "-" }}</dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">4K Controllers</dt>
          <dd class="font-semibold">{{ selectedVariant ? calculations.controllers4k.value : "-" }}</dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Power Requirements Max</dt>
          <dd class="font-semibold">{{ formatPower(calculations.maxPowerW.value) }}</dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Power Requirements Typical</dt>
          <dd class="font-semibold">{{ formatPower(calculations.typicalPowerW.value) }}</dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Heat Generation Max</dt>
          <dd class="font-semibold">{{ formatHeat(calculations.maxHeatBtuH.value) }}</dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Heat Generation Typical</dt>
          <dd class="font-semibold">{{ formatHeat(calculations.typicalHeatBtuH.value) }}</dd>
        </div>
      </dl>
    </section>
  </div>
</template>
