<script setup lang="ts">
import type { LedModel, LedModelDetail, LedVariant } from "~/types/led";

const props = defineProps<{
  models: LedModel[];
  loading: boolean;
  hasError: boolean;
}>();

const emit = defineEmits<{
  (event: "close"): void;
  (event: "confirm", payload: { model: LedModel; variant: LedVariant }): void;
}>();

const { fetchLedModelDetail } = useLedApi();
const { resolveLedImage } = useLedImages();

const step = ref<1 | 2>(1);
const detailLoading = ref(false);
const detailError = ref(false);
const modelDetail = ref<LedModelDetail | null>(null);
const selectedModel = ref<LedModel | null>(null);
const selectedVariant = ref<LedVariant | null>(null);

const selectedModelImage = computed(() =>
  resolveLedImage(selectedModel.value?.main_image || selectedModel.value?.thumbnail_image),
);

const variants = computed(() => modelDetail.value?.variants ?? []);

const resetModal = () => {
  step.value = 1;
  detailLoading.value = false;
  detailError.value = false;
  modelDetail.value = null;
  selectedModel.value = null;
  selectedVariant.value = null;
};

const closeModal = () => {
  resetModal();
  emit("close");
};

const selectModel = (model: LedModel) => {
  selectedModel.value = model;
};

const loadSelectedModelDetail = async () => {
  if (!selectedModel.value) {
    return;
  }

  detailLoading.value = true;
  detailError.value = false;
  selectedVariant.value = null;

  try {
    modelDetail.value = await fetchLedModelDetail(selectedModel.value.slug);
    step.value = 2;
  } catch {
    detailError.value = true;
  } finally {
    detailLoading.value = false;
  }
};

const goBack = () => {
  if (step.value === 1) {
    return;
  }

  step.value = 1;
  selectedVariant.value = null;
};

const goNext = async () => {
  if (step.value === 1) {
    await loadSelectedModelDetail();
    return;
  }

  if (selectedModel.value && selectedVariant.value) {
    emit("confirm", {
      model: selectedModel.value,
      variant: selectedVariant.value,
    });
    resetModal();
  }
};

const formatDimensions = (variant: LedVariant) => {
  return `${variant.cabinet_width_mm} x ${variant.cabinet_height_mm} x ${
    variant.cabinet_depth_mm ?? "-"
  } mm`;
};
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/45 px-4 py-6">
      <section
        class="relative box-border flex max-h-[92vh] w-full max-w-4xl flex-col overflow-hidden rounded-xl bg-white shadow-2xl"
      >
        <button
          type="button"
          class="absolute right-6 top-6 z-10 flex h-10 w-10 items-center justify-center text-4xl font-light"
          aria-label="Close modal"
          @click="closeModal"
        >
          x
        </button>

        <div class="flex-1 overflow-y-auto px-6 py-8 sm:px-10 lg:px-12">
          <template v-if="step === 1">
            <h2 class="text-3xl font-black tracking-normal">Select model</h2>

            <p v-if="loading" class="mt-8 text-neutral-500">Loading LED models...</p>
            <p v-else-if="hasError" class="mt-8 text-red-600">Could not load LED models.</p>

            <div v-else class="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2">
              <button
                v-for="model in props.models"
                :key="model.id"
                type="button"
                class="flex min-h-40 w-full flex-col rounded-2xl border p-4 text-left transition hover:border-blue-600"
                :class="
                  selectedModel?.id === model.id
                    ? 'border-blue-600 bg-blue-50'
                    : 'border-neutral-200 bg-white'
                "
                @click="selectModel(model)"
              >
                <div class="flex items-start justify-between gap-4">
                  <div>
                    <p class="text-xs font-bold uppercase text-blue-600">
                      {{ model.product_type }}
                    </p>
                    <h3 class="mt-1 text-xl font-black tracking-normal">{{ model.name }}</h3>
                    <p class="mt-1 text-sm text-neutral-500">{{ model.subtitle }}</p>
                  </div>

                  <img
                    v-if="resolveLedImage(model.thumbnail_image || model.main_image)"
                    :src="resolveLedImage(model.thumbnail_image || model.main_image)"
                    :alt="model.name"
                    class="h-20 w-28 object-contain"
                  >
                  <div v-else class="h-20 w-28 rounded-lg bg-neutral-100" />
                </div>

                <p class="mt-auto pt-5 text-sm font-semibold text-neutral-500">
                  {{ model.variants_count }} variants
                </p>
              </button>
            </div>
          </template>

          <template v-else>
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 class="text-3xl font-black tracking-normal">
                  {{ modelDetail?.name || selectedModel?.name }}
                </h2>
                <p class="mt-1 text-sm text-neutral-500">
                  Select a cabinet variant for this configuration.
                </p>
              </div>

              <img
                v-if="selectedModelImage"
                :src="selectedModelImage"
                :alt="selectedModel?.name"
                class="h-20 w-32 object-contain"
              >
            </div>

            <p v-if="detailLoading" class="mt-8 text-neutral-500">Loading variants...</p>
            <p v-else-if="detailError" class="mt-8 text-red-600">Could not load variants.</p>

            <div v-else class="mt-8 overflow-x-auto">
              <table class="min-w-[760px] w-full border-separate border-spacing-y-2 text-sm">
                <thead>
                  <tr class="bg-blue-600 text-white">
                    <th class="rounded-l-full px-5 py-4 text-left font-bold">Model Name</th>
                    <th class="px-4 py-4 text-left font-bold">Pixel Pitch</th>
                    <th class="px-4 py-4 text-left font-bold">Brightness</th>
                    <th class="px-4 py-4 text-left font-bold">Dimensions</th>
                    <th class="px-4 py-4 text-left font-bold">Refresh Rate</th>
                    <th class="rounded-r-full px-5 py-4 text-left font-bold">
                      Web Price / Cabinet
                    </th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="variant in variants"
                    :key="variant.id"
                    class="cursor-pointer bg-white transition"
                    :class="
                      selectedVariant?.id === variant.id
                        ? 'outline outline-2 outline-blue-600'
                        : 'hover:bg-neutral-50'
                    "
                    @click="selectedVariant = variant"
                  >
                    <td class="rounded-l-full px-5 py-4">{{ variant.model_name }}</td>
                    <td class="px-4 py-4">{{ variant.pixel_pitch }}</td>
                    <td class="px-4 py-4">{{ variant.brightness_nits }} nits</td>
                    <td class="px-4 py-4">{{ formatDimensions(variant) }}</td>
                    <td class="px-4 py-4">{{ variant.refresh_rate_hz }} Hz</td>
                    <td class="rounded-r-full px-5 py-4">
                      {{ variant.web_price_per_cabinet ?? "-" }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
        </div>

        <footer class="flex items-center justify-center gap-6 px-6 py-8">
          <button
            type="button"
            class="h-11 min-w-36 rounded-full border border-neutral-950 px-6 text-sm font-semibold disabled:border-neutral-300 disabled:text-neutral-400"
            :disabled="step === 1"
            @click="goBack"
          >
            Back
          </button>

          <button
            type="button"
            class="h-11 min-w-36 rounded-full bg-blue-600 px-6 text-sm font-semibold text-white disabled:bg-neutral-300"
            :disabled="step === 1 ? !selectedModel || detailLoading : !selectedVariant"
            @click="goNext"
          >
            {{ step === 1 ? "Next" : "Confirm" }}
          </button>
        </footer>
      </section>
    </div>
  </Teleport>
</template>
