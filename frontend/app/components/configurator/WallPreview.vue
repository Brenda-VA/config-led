<script setup lang="ts">
import previewImageSrc from "../../../assets/recursos/preview-imagen.png";
import previewVideoSrc from "../../../assets/recursos/preview-video.webm";
import referenceWomanSrc from "../../../assets/recursos/referencia-mujer.png";
import type { ConfigUnit, ContentMode, LedVariant } from "~/types/led";

const props = defineProps<{
  selectedVariant: LedVariant | null;
  wallWidth: number;
  wallHeight: number;
  unit: ConfigUnit;
  columns: number;
  rows: number;
  contentMode: ContentMode;
}>();

const emit = defineEmits<{
  (event: "start-config"): void;
  (event: "reset"): void;
}>();

const calculations = useLedCalculations({
  selectedVariant: toRef(props, "selectedVariant"),
  wallWidth: toRef(props, "wallWidth"),
  wallHeight: toRef(props, "wallHeight"),
  unit: toRef(props, "unit"),
  columns: toRef(props, "columns"),
  rows: toRef(props, "rows"),
});

const previewBox = computed(() => {
  const maxWidth = 760;
  const maxHeight = 390;
  const wallWidth = calculations.wallWidthM.value || 5;
  const wallHeight = calculations.wallHeightM.value || 3;
  const wallAspect = wallWidth / wallHeight;
  const previewAspect = maxWidth / maxHeight;

  if (wallAspect >= previewAspect) {
    return {
      width: maxWidth,
      height: maxWidth / wallAspect,
    };
  }

  return {
    width: maxHeight * wallAspect,
    height: maxHeight,
  };
});

const screenPercent = computed(() => {
  const widthPercent = calculations.wallWidthM.value
    ? Math.min((calculations.displayWidthM.value / calculations.wallWidthM.value) * 100, 100)
    : 0;
  const heightPercent = calculations.wallHeightM.value
    ? Math.min((calculations.displayHeightM.value / calculations.wallHeightM.value) * 100, 100)
    : 0;

  return {
    width: Math.max(widthPercent, 2),
    height: Math.max(heightPercent, 2),
    left: Math.max((100 - widthPercent) / 2, 0),
    top: Math.max((100 - heightPercent) / 2, 0),
  };
});

const wallStyle = computed(() => ({
  width: `${previewBox.value.width}px`,
  height: `${previewBox.value.height}px`,
}));

const screenStyle = computed(() => ({
  left: `${screenPercent.value.left}%`,
  top: `${screenPercent.value.top}%`,
  width: `${screenPercent.value.width}%`,
  height: `${screenPercent.value.height}%`,
}));

const screenWidthLabelStyle = computed(() => ({
  left: `${screenPercent.value.left + screenPercent.value.width / 2}%`,
}));

const screenHeightLabelStyle = computed(() => ({
  left: `${Math.min(screenPercent.value.left + screenPercent.value.width + 2, 94)}%`,
  top: `${screenPercent.value.top + screenPercent.value.height / 2}%`,
}));

const formatMeters = (value: number, digits = 2) => `${value.toFixed(digits)} m`;
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
      <div class="relative flex min-h-[430px] min-w-[760px] items-center justify-center">
        <div class="relative border border-slate-300 bg-white" :style="wallStyle">
          <div
            class="absolute -top-12 rounded bg-neutral-400 px-6 py-2 text-sm font-bold text-white"
            :style="{ left: '8%' }"
          >
            {{ formatMeters(calculations.sideClearanceM.value) }}
          </div>

          <div
            class="absolute -top-12 rounded bg-neutral-400 px-6 py-2 text-sm font-bold text-white"
            :style="{ right: '8%' }"
          >
            {{ formatMeters(calculations.sideClearanceM.value) }}
          </div>

          <div
            class="absolute -top-12 -translate-x-1/2 rounded bg-neutral-900 px-5 py-2 text-sm font-bold text-white"
            :style="screenWidthLabelStyle"
          >
            {{ formatMeters(calculations.displayWidthM.value) }}
          </div>

          <div
            class="absolute -right-24 rounded bg-neutral-400 px-3 py-2 text-sm font-bold text-white"
            :style="{ top: '12%' }"
          >
            {{ formatMeters(calculations.verticalClearanceM.value) }}
          </div>

          <div
            class="absolute -right-24 rounded bg-neutral-400 px-3 py-2 text-sm font-bold text-white"
            :style="{ bottom: '12%' }"
          >
            {{ formatMeters(calculations.verticalClearanceM.value) }}
          </div>

          <div
            class="absolute -translate-y-1/2 rounded bg-neutral-900 px-3 py-2 text-sm font-bold text-white"
            :style="screenHeightLabelStyle"
          >
            {{ formatMeters(calculations.displayHeightM.value, 3) }}
          </div>

          <div
            class="absolute border border-dashed border-black bg-neutral-200"
            :style="screenStyle"
          >
            <img
              v-if="contentMode === 'default'"
              :src="previewImageSrc"
              alt=""
              class="h-full w-full object-cover"
            >
            <video
              v-else-if="contentMode === 'preview'"
              :src="previewVideoSrc"
              class="h-full w-full object-cover"
              autoplay
              loop
              muted
              playsinline
            />
            <div
              v-else-if="contentMode === 'upload'"
              class="flex h-full w-full items-center justify-center bg-neutral-800 text-xs font-bold text-white"
            >
              Upload
            </div>
            <div v-else class="h-full w-full bg-white" />
          </div>
        </div>

        <div class="absolute bottom-0 left-2 flex flex-col items-center">
          <img :src="referenceWomanSrc" alt="" class="h-36 w-auto opacity-60">
          <p class="mt-1 text-xs font-medium text-neutral-950">* Woman: 1.60 m</p>
        </div>
      </div>
    </div>
  </div>
</template>
