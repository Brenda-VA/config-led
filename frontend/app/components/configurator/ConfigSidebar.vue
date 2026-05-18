<script setup lang="ts">
import type { LedModel, LedVariant } from "~/types/led";

defineProps<{
  selectedModel: LedModel | null;
  selectedVariant: LedVariant | null;
  modelImageSrc: string;
}>();

const emit = defineEmits<{
  (event: "change-model"): void;
}>();

const formatCabinetSize = (variant: LedVariant | null) => {
  if (!variant) {
    return "-";
  }

  return `${variant.cabinet_width_mm} x ${variant.cabinet_height_mm} x ${
    variant.cabinet_depth_mm ?? "-"
  } mm`;
};
</script>

<template>
  <div class="space-y-3">
    <section class="rounded-xl bg-white p-5 shadow-lg shadow-neutral-200/70">
      <button
        type="button"
        class="flex w-full items-start justify-between gap-4 text-left"
        @click="emit('change-model')"
      >
        <div>
          <h2 class="text-3xl font-black tracking-normal">Model</h2>
          <div class="mt-3 h-px w-full bg-neutral-200" />
        </div>
        <span class="text-3xl leading-none text-neutral-500">&gt;</span>
      </button>

      <div v-if="selectedModel && selectedVariant" class="mt-5 flex items-center gap-4">
        <div class="min-w-0 flex-1">
          <p class="text-sm font-semibold text-neutral-400">
            {{ selectedVariant.model_name }}
          </p>
          <p class="text-2xl font-black">{{ selectedVariant.pixel_pitch }} mm</p>
          <dl class="mt-3 space-y-1 text-sm text-neutral-600">
            <div>
              <dt class="font-semibold">Cabinet</dt>
              <dd>{{ formatCabinetSize(selectedVariant) }}</dd>
            </div>
            <div>
              <dt class="font-semibold">Refresh</dt>
              <dd>{{ selectedVariant.refresh_rate_hz }} Hz</dd>
            </div>
          </dl>
        </div>

        <img
          v-if="modelImageSrc"
          :src="modelImageSrc"
          :alt="selectedModel.name"
          class="h-20 w-28 object-contain"
        >
        <div v-else class="h-20 w-28 rounded-lg bg-neutral-100" />
      </div>

      <p v-else class="mt-5 max-w-[180px] text-xl font-semibold text-neutral-400">
        Select your model
      </p>
    </section>

    <section
      class="rounded-xl bg-white p-5 shadow-lg shadow-neutral-200/70"
      :class="!selectedVariant ? 'opacity-60' : ''"
    >
      <h2 class="text-3xl font-black tracking-normal">Room</h2>
      <div class="mt-3 h-px w-full bg-neutral-200" />

      <div class="mt-5 space-y-5 text-sm">
        <div>
          <p class="mb-3 font-semibold text-neutral-500">Unit</p>
          <div class="flex items-center justify-between gap-4">
            <label class="flex items-center gap-2">
              <input type="radio" checked class="h-5 w-5" :disabled="!selectedVariant">
              <span>Meters</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="radio" class="h-5 w-5" :disabled="!selectedVariant">
              <span>Feet</span>
            </label>
          </div>
        </div>

        <label class="flex items-center justify-between gap-4">
          <span class="font-semibold text-neutral-500">Wall Width</span>
          <input
            type="number"
            value="5"
            class="h-9 w-16 rounded border border-neutral-300 px-2 text-right"
            :disabled="!selectedVariant"
          >
        </label>

        <label class="flex items-center justify-between gap-4">
          <span class="font-semibold text-neutral-500">Wall Height</span>
          <input
            type="number"
            value="3"
            class="h-9 w-16 rounded border border-neutral-300 px-2 text-right"
            :disabled="!selectedVariant"
          >
        </label>
      </div>
    </section>

    <section
      class="rounded-xl bg-white p-5 shadow-lg shadow-neutral-200/70"
      :class="!selectedVariant ? 'opacity-60' : ''"
    >
      <h2 class="text-3xl font-black tracking-normal">Display</h2>
      <div class="mt-3 h-px w-full bg-neutral-200" />

      <div class="mt-5 space-y-4 text-sm">
        <label class="flex items-center justify-between gap-4">
          <span class="font-semibold text-neutral-500">Columns</span>
          <input
            type="number"
            value="1"
            class="h-9 w-16 rounded border border-neutral-300 px-2 text-right"
            :disabled="!selectedVariant"
          >
        </label>

        <label class="flex items-center justify-between gap-4">
          <span class="font-semibold text-neutral-500">Rows</span>
          <input
            type="number"
            value="1"
            class="h-9 w-16 rounded border border-neutral-300 px-2 text-right"
            :disabled="!selectedVariant"
          >
        </label>

        <div>
          <p class="mb-2 font-semibold text-neutral-500">Resolution</p>
          <div class="grid grid-cols-2 gap-3">
            <button type="button" class="h-10 rounded border border-neutral-300" :disabled="!selectedVariant">
              FHD
            </button>
            <button type="button" class="h-10 rounded border border-neutral-300" :disabled="!selectedVariant">
              UHD
            </button>
          </div>
        </div>

        <div>
          <p class="mb-2 font-semibold text-neutral-500">Configuration</p>
          <button
            type="button"
            class="h-10 w-full rounded border border-neutral-300"
            :disabled="!selectedVariant"
          >
            Fit To Wall
          </button>
        </div>

        <div>
          <p class="mb-2 font-semibold text-neutral-500">Redundancy</p>
          <div class="flex items-center justify-between gap-3">
            <label class="flex items-center gap-2">
              <input type="checkbox" checked :disabled="!selectedVariant">NO
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" :disabled="!selectedVariant">POWER
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" :disabled="!selectedVariant">DATA
            </label>
          </div>
        </div>

        <div>
          <p class="mb-2 font-semibold text-neutral-500">Content</p>
          <div class="grid grid-cols-2 gap-2">
            <button
              type="button"
              class="h-16 rounded bg-[linear-gradient(135deg,#111827,#7c3aed,#ef4444)] text-sm font-black text-white"
              :disabled="!selectedVariant"
            >
              DEFAULT IMAGE
            </button>
            <button
              type="button"
              class="h-16 rounded bg-[linear-gradient(135deg,#0f172a,#2563eb,#f43f5e)] text-sm font-black text-white"
              :disabled="!selectedVariant"
            >
              PREVIEW VIDEO
            </button>
            <button
              type="button"
              class="h-10 rounded border border-neutral-300 text-sm"
              :disabled="!selectedVariant"
            >
              Upload Image
            </button>
            <button
              type="button"
              class="h-10 rounded border border-neutral-300 text-sm"
              :disabled="!selectedVariant"
            >
              No Image
            </button>
          </div>
        </div>
      </div>
    </section>

    <section class="rounded-xl bg-white p-5 shadow-lg shadow-neutral-200/70">
      <h2 class="text-2xl font-black tracking-normal">Controller</h2>
      <p class="mt-3 text-sm font-semibold text-neutral-400">No controller selected</p>
    </section>

    <section class="rounded-xl bg-white p-5 shadow-lg shadow-neutral-200/70">
      <h2 class="text-2xl font-black tracking-normal">LED Display Price</h2>
      <p class="mt-3 text-sm font-semibold text-neutral-400">
        {{ selectedVariant?.web_price_per_cabinet ?? "-" }}
      </p>
    </section>
  </div>
</template>
