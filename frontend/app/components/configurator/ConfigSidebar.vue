<script setup lang="ts">
import previewImageSrc from "../../../assets/recursos/preview-imagen.png";
import previewVideoSrc from "../../../assets/recursos/preview-video.webm";
import type {
  ConfigUnit,
  ContentMode,
  LedController,
  LedModel,
  LedVariant,
  RedundancyMode,
  ResolutionMode,
} from "~/types/led";

// La sidebar no guarda el estado final; solo emite cambios hacia la pagina padre.
const props = defineProps<{
  selectedModel: LedModel | null;
  selectedVariant: LedVariant | null;
  modelImageSrc: string;
  wallWidth: number;
  wallHeight: number;
  unit: ConfigUnit;
  columns: number;
  rows: number;
  resolutionMode: ResolutionMode;
  redundancy: RedundancyMode;
  contentMode: ContentMode;
  controllers: LedController[];
  controllersLoading: boolean;
  controllersError: boolean;
  selectedController: LedController | null;
  controllerQuantity: number;
  saveStatus: "idle" | "saving" | "success" | "error";
  saveMessage: string;
}>();

const emit = defineEmits<{
  (event: "requestModelChange"): void;
  (event: "update:wallWidth", value: number): void;
  (event: "update:wallHeight", value: number): void;
  (event: "update:unit", value: ConfigUnit): void;
  (event: "update:columns", value: number): void;
  (event: "update:rows", value: number): void;
  (event: "update:resolutionMode", value: ResolutionMode): void;
  (event: "update:redundancy", value: RedundancyMode): void;
  (event: "update:contentMode", value: ContentMode): void;
  (event: "update:selectedController", value: LedController | null): void;
  (event: "update:controllerQuantity", value: number): void;
  (event: "exportPdf"): void;
}>();

const formatCabinetSize = (variant: LedVariant | null) => {
  if (!variant) {
    return "-";
  }

  return `${variant.cabinet_width_mm} x ${variant.cabinet_height_mm} x ${
    variant.cabinet_depth_mm ?? "-"
  } mm`;
};

const readNumberInput = (event: Event, fallback: number, minimum = 0) => {
  const input = event.target as HTMLInputElement;
  const parsedValue = Number(input.value);

  if (!Number.isFinite(parsedValue)) {
    return fallback;
  }

  return Math.max(minimum, parsedValue);
};

const readIntegerInput = (event: Event, fallback: number) => {
  return Math.max(1, Math.round(readNumberInput(event, fallback, 1)));
};

const availableControllerBrands = computed(() => {
  return Array.from(new Set(props.controllers.map((controller) => controller.brand)));
});

const activeControllerBrand = computed(() => {
  return props.selectedController?.brand ?? availableControllerBrands.value[0] ?? "";
});

const controllersByActiveBrand = computed(() => {
  return props.controllers.filter((controller) => controller.brand === activeControllerBrand.value);
});

const formatBrand = (brand: string) => {
  if (!brand) {
    return "-";
  }

  return brand.charAt(0).toUpperCase() + brand.slice(1);
};

const formatPrice = (price: string | null) => {
  if (!price) {
    return "-";
  }

  return Number(price).toLocaleString(undefined, {
    style: "currency",
    currency: "EUR",
  });
};

const selectedControllerTotalPrice = computed(() => {
  if (!props.selectedController?.price) {
    return "-";
  }

  return formatPrice(String(Number(props.selectedController.price) * props.controllerQuantity));
});

const selectControllerBrand = (event: Event) => {
  const input = event.target as HTMLSelectElement;
  const firstControllerForBrand =
    props.controllers.find((controller) => controller.brand === input.value) ?? null;

  emit("update:selectedController", firstControllerForBrand);
};

const selectController = (event: Event) => {
  const input = event.target as HTMLSelectElement;
  const controllerId = Number(input.value);

  emit(
    "update:selectedController",
    props.controllers.find((controller) => controller.id === controllerId) ?? null,
  );
};
</script>

<template>
  <div class="space-y-3">
    <section class="rounded-xl bg-white p-5 shadow-lg shadow-neutral-200/70">
      <button
        type="button"
        class="flex w-full items-start justify-between gap-4 text-left"
        @click="emit('requestModelChange')"
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
              <input
                type="radio"
                class="h-5 w-5"
                :checked="unit === 'meters'"
                :disabled="!selectedVariant"
                @change="emit('update:unit', 'meters')"
              >
              <span>Meters</span>
            </label>
            <label class="flex items-center gap-2">
              <input
                type="radio"
                class="h-5 w-5"
                :checked="unit === 'feet'"
                :disabled="!selectedVariant"
                @change="emit('update:unit', 'feet')"
              >
              <span>Feet</span>
            </label>
          </div>
        </div>

        <label class="flex items-center justify-between gap-4">
          <span class="font-semibold text-neutral-500">Wall Width</span>
          <input
            type="number"
            :value="wallWidth"
            min="0.1"
            step="0.1"
            class="h-9 w-16 rounded border border-neutral-300 px-2 text-right"
            :disabled="!selectedVariant"
            @input="emit('update:wallWidth', readNumberInput($event, wallWidth, 0.1))"
          >
        </label>

        <label class="flex items-center justify-between gap-4">
          <span class="font-semibold text-neutral-500">Wall Height</span>
          <input
            type="number"
            :value="wallHeight"
            min="0.1"
            step="0.1"
            class="h-9 w-16 rounded border border-neutral-300 px-2 text-right"
            :disabled="!selectedVariant"
            @input="emit('update:wallHeight', readNumberInput($event, wallHeight, 0.1))"
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
            :value="columns"
            min="1"
            step="1"
            class="h-9 w-16 rounded border border-neutral-300 px-2 text-right"
            :disabled="!selectedVariant"
            @input="emit('update:columns', readIntegerInput($event, columns))"
          >
        </label>

        <label class="flex items-center justify-between gap-4">
          <span class="font-semibold text-neutral-500">Rows</span>
          <input
            type="number"
            :value="rows"
            min="1"
            step="1"
            class="h-9 w-16 rounded border border-neutral-300 px-2 text-right"
            :disabled="!selectedVariant"
            @input="emit('update:rows', readIntegerInput($event, rows))"
          >
        </label>

        <div>
          <p class="mb-2 font-semibold text-neutral-500">Resolution</p>
          <div class="grid grid-cols-2 gap-3">
            <button
              type="button"
              class="h-10 rounded border border-neutral-300"
              :class="resolutionMode === 'FHD' ? 'border-blue-600 bg-blue-50 text-blue-700' : ''"
              :disabled="!selectedVariant"
              @click="emit('update:resolutionMode', 'FHD')"
            >
              FHD
            </button>
            <button
              type="button"
              class="h-10 rounded border border-neutral-300"
              :class="resolutionMode === 'UHD' ? 'border-blue-600 bg-blue-50 text-blue-700' : ''"
              :disabled="!selectedVariant"
              @click="emit('update:resolutionMode', 'UHD')"
            >
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
              <input
                type="checkbox"
                :checked="redundancy === 'NO'"
                :disabled="!selectedVariant"
                @change="emit('update:redundancy', 'NO')"
              >NO
            </label>
            <label class="flex items-center gap-2">
              <input
                type="checkbox"
                :checked="redundancy === 'POWER'"
                :disabled="!selectedVariant"
                @change="emit('update:redundancy', 'POWER')"
              >POWER
            </label>
            <label class="flex items-center gap-2">
              <input
                type="checkbox"
                :checked="redundancy === 'DATA'"
                :disabled="!selectedVariant"
                @change="emit('update:redundancy', 'DATA')"
              >DATA
            </label>
          </div>
        </div>

        <div>
          <p class="mb-2 font-semibold text-neutral-500">Content</p>
          <div class="grid grid-cols-2 gap-2">
            <button
              type="button"
              class="relative h-16 overflow-hidden rounded border text-sm font-black text-white"
              :class="contentMode === 'default' ? 'border-blue-600 ring-2 ring-blue-600' : 'border-transparent'"
              :disabled="!selectedVariant"
              @click="emit('update:contentMode', 'default')"
            >
              <img :src="previewImageSrc" alt="" class="absolute inset-0 h-full w-full object-cover">
              <span class="relative">DEFAULT IMAGE</span>
            </button>
            <button
              type="button"
              class="relative h-16 overflow-hidden rounded border text-sm font-black text-white"
              :class="contentMode === 'preview' ? 'border-blue-600 ring-2 ring-blue-600' : 'border-transparent'"
              :disabled="!selectedVariant"
              @click="emit('update:contentMode', 'preview')"
            >
              <video
                :src="previewVideoSrc"
                class="absolute inset-0 h-full w-full object-cover"
                autoplay
                loop
                muted
                playsinline
              />
              <span class="relative">PREVIEW VIDEO</span>
            </button>
            <button
              type="button"
              class="h-10 rounded border border-neutral-300 text-sm"
              :class="contentMode === 'upload' ? 'border-blue-600 bg-blue-50 text-blue-700' : ''"
              :disabled="!selectedVariant"
              @click="emit('update:contentMode', 'upload')"
            >
              Upload Image
            </button>
            <button
              type="button"
              class="h-10 rounded border border-neutral-300 text-sm"
              :class="contentMode === 'none' ? 'border-blue-600 bg-blue-50 text-blue-700' : ''"
              :disabled="!selectedVariant"
              @click="emit('update:contentMode', 'none')"
            >
              No Image
            </button>
          </div>
        </div>
      </div>
    </section>

    <section class="rounded-xl bg-white p-5 shadow-lg shadow-neutral-200/70">
      <h2 class="text-2xl font-black tracking-normal">Controller</h2>

      <p v-if="controllersLoading" class="mt-3 text-sm font-semibold text-neutral-400">
        Loading controllers...
      </p>
      <p v-else-if="controllersError" class="mt-3 text-sm font-semibold text-red-600">
        Controllers could not be loaded.
      </p>
      <p v-else-if="!controllers.length" class="mt-3 text-sm font-semibold text-neutral-400">
        No controllers available.
      </p>

      <div v-else class="mt-4 space-y-4 text-sm">
        <label class="block">
          <span class="mb-2 block font-semibold text-neutral-500">Brand</span>
          <select
            class="h-10 w-full rounded border border-neutral-300 px-3"
            :value="activeControllerBrand"
            :disabled="!selectedVariant"
            @change="selectControllerBrand"
          >
            <option
              v-for="brand in availableControllerBrands"
              :key="brand"
              :value="brand"
            >
              {{ formatBrand(brand) }}
            </option>
          </select>
        </label>

        <label class="block">
          <span class="mb-2 block font-semibold text-neutral-500">Controller</span>
          <select
            class="h-10 w-full rounded border border-neutral-300 px-3"
            :value="selectedController?.id ?? ''"
            :disabled="!selectedVariant"
            @change="selectController"
          >
            <option value="">Select controller</option>
            <option
              v-for="controller in controllersByActiveBrand"
              :key="controller.id"
              :value="controller.id"
            >
              {{ controller.name }} · {{ formatPrice(controller.price) }}
            </option>
          </select>
        </label>

        <label class="flex items-center justify-between gap-4">
          <span class="font-semibold text-neutral-500">Quantity</span>
          <input
            type="number"
            :value="controllerQuantity"
            min="1"
            step="1"
            class="h-9 w-16 rounded border border-neutral-300 px-2 text-right"
            :disabled="!selectedVariant"
            @input="emit('update:controllerQuantity', readIntegerInput($event, controllerQuantity))"
          >
        </label>

        <p class="font-semibold text-neutral-500">
          Controller total:
          <span class="text-neutral-950">{{ selectedControllerTotalPrice }}</span>
        </p>
      </div>
    </section>

    <section class="rounded-xl bg-white p-5 shadow-lg shadow-neutral-200/70">
      <h2 class="text-2xl font-black tracking-normal">LED Display Price</h2>
      <p class="mt-3 text-sm font-semibold text-neutral-400">
        {{ selectedVariant?.web_price_per_cabinet ?? "-" }}
      </p>

      <button
        type="button"
        class="mt-5 h-12 w-full rounded-full bg-blue-600 px-5 text-sm font-semibold text-white disabled:bg-neutral-300"
        :disabled="!selectedVariant || saveStatus === 'saving'"
        @click="emit('exportPdf')"
      >
        {{ saveStatus === "saving" ? "Saving..." : "Export PDF" }}
      </button>

      <p
        v-if="saveMessage"
        class="mt-3 text-sm font-semibold"
        :class="saveStatus === 'success' ? 'text-green-600' : 'text-red-600'"
      >
        {{ saveMessage }}
      </p>
    </section>
  </div>
</template>
