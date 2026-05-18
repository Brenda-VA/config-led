<script setup lang="ts">
import type { LedVariant } from "~/types/led";

const props = defineProps<{
  selectedVariant: LedVariant | null;
}>();

const emit = defineEmits<{
  (event: "start-config"): void;
  (event: "reset"): void;
}>();

const cabinetWidthMeters = computed(() => {
  if (!props.selectedVariant) {
    return "0.6";
  }

  return (Number(props.selectedVariant.cabinet_width_mm) / 1000).toFixed(1);
});

const cabinetHeightMeters = computed(() => {
  if (!props.selectedVariant) {
    return "0.338";
  }

  return (Number(props.selectedVariant.cabinet_height_mm) / 1000).toFixed(3);
});
</script>

<template>
  <div class="relative box-border flex h-full min-h-[480px] w-full flex-col">
    <div v-if="selectedVariant" class="flex items-center gap-3">
      <button
        type="button"
        class="inline-flex h-14 items-center gap-3 rounded bg-black px-5 text-sm font-semibold text-white"
      >
        <span class="h-8 w-8 border border-white" aria-hidden="true" />
        Mark
      </button>

      <button
        type="button"
        class="inline-flex h-14 items-center gap-3 rounded bg-black px-5 text-sm font-semibold text-white"
        @click="emit('reset')"
      >
        <span class="h-8 w-8 rounded-full border-2 border-white" aria-hidden="true" />
        Reset
      </button>
    </div>

    <div
      v-if="!selectedVariant"
      class="flex min-h-[420px] flex-1 flex-col items-center justify-center text-center"
    >
      <div class="mb-5 flex h-16 w-20 items-center justify-center rounded border-2 border-black">
        <div class="h-7 w-10 border-2 border-black" />
      </div>

      <p class="mb-5 text-base font-medium text-neutral-950">
        Please select a product model for configuration
      </p>

      <button
        type="button"
        class="h-12 rounded-full bg-blue-600 px-7 text-sm font-semibold text-white shadow-sm"
        @click="emit('start-config')"
      >
        Start configuration
      </button>
    </div>

    <div v-else class="flex min-h-[520px] flex-1 items-center justify-center overflow-x-auto py-8">
      <div class="relative h-[360px] w-[760px] min-w-[680px]">
        <div
          class="absolute left-16 top-24 h-[250px] w-[600px] border border-slate-300 bg-white"
        />

        <div
          class="absolute left-[330px] top-[205px] h-[46px] w-[84px] border border-dashed border-black bg-[linear-gradient(135deg,#111827,#7c3aed,#0ea5e9)]"
        />

        <div
          class="absolute left-[330px] top-[120px] h-[132px] w-[84px] border border-dashed border-black"
        />

        <div
          class="absolute left-[330px] top-[104px] rounded bg-neutral-900 px-5 py-2 text-sm font-bold text-white"
        >
          {{ cabinetWidthMeters }} m
        </div>

        <div
          class="absolute right-6 top-[200px] rounded bg-neutral-900 px-3 py-2 text-sm font-bold text-white"
        >
          {{ cabinetHeightMeters }} m
        </div>

        <div class="absolute left-16 top-10 rounded bg-neutral-400 px-6 py-2 text-sm font-bold text-white">
          2.2 m
        </div>

        <div class="absolute right-16 top-10 rounded bg-neutral-400 px-6 py-2 text-sm font-bold text-white">
          2.2 m
        </div>

        <div class="absolute bottom-8 left-2 text-xs font-medium text-neutral-950">
          * Woman: 1.60 m
        </div>
      </div>
    </div>
  </div>
</template>
