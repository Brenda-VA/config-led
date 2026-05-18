<script setup lang="ts">
import type { LedVariant } from "~/types/led";

const props = defineProps<{
  selectedVariant: LedVariant | null;
}>();

const totalPixels = computed(() => {
  if (!props.selectedVariant) {
    return "-";
  }

  return (
    props.selectedVariant.resolution_width_px_per_cabinet *
    props.selectedVariant.resolution_height_px_per_cabinet
  ).toLocaleString();
});
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
          <dt class="font-semibold text-neutral-500">Resolution</dt>
          <dd class="font-semibold">
            <template v-if="selectedVariant">
              {{ selectedVariant.resolution_width_px_per_cabinet }} x
              {{ selectedVariant.resolution_height_px_per_cabinet }}
            </template>
            <template v-else>-</template>
          </dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Total pixel quantity</dt>
          <dd class="font-semibold">{{ totalPixels }}</dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Max power</dt>
          <dd class="font-semibold">
            {{ selectedVariant ? `${selectedVariant.max_power_w} W` : "-" }}
          </dd>
        </div>

        <div class="flex justify-between gap-4">
          <dt class="font-semibold text-neutral-500">Typical power</dt>
          <dd class="font-semibold">
            {{ selectedVariant ? `${selectedVariant.typical_power_w} W` : "-" }}
          </dd>
        </div>
      </dl>
    </section>
  </div>
</template>
