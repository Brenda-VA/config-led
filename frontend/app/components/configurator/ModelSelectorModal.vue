<script setup lang="ts">
import type { LedModel, LedModelDetail, LedVariant, ProductType } from "~/types/led";

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
const activeProductType = ref<ProductType>("indoor");
const detailLoading = ref(false);
const detailError = ref(false);
const modelDetail = ref<LedModelDetail | null>(null);
const selectedModel = ref<LedModel | null>(null);
const selectedVariant = ref<LedVariant | null>(null);

const activeModels = computed(() =>
  props.models.filter((model) => model.product_type === activeProductType.value),
);

const activeModelIndex = computed(() => {
  if (!selectedModel.value) {
    return -1;
  }

  return activeModels.value.findIndex((model) => model.id === selectedModel.value?.id);
});

const isIndoorStep = computed(() => step.value === 1 && activeProductType.value === "indoor");

const selectedModelImage = computed(() =>
  resolveLedImage(selectedModel.value?.main_image || selectedModel.value?.thumbnail_image),
);

const variants = computed(() => modelDetail.value?.variants ?? []);

const resetModal = () => {
  step.value = 1;
  activeProductType.value = "indoor";
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

const selectProductType = (productType: ProductType) => {
  activeProductType.value = productType;
  modelDetail.value = null;
  selectedVariant.value = null;
};

const selectModelByOffset = (offset: number) => {
  if (!activeModels.value.length) {
    return;
  }

  const currentIndex = activeModelIndex.value >= 0 ? activeModelIndex.value : 0;
  const nextIndex = (currentIndex + offset + activeModels.value.length) % activeModels.value.length;
  selectedModel.value = activeModels.value[nextIndex];
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

watch(
  activeModels,
  (models) => {
    if (!models.some((model) => model.id === selectedModel.value?.id)) {
      selectedModel.value = models[0] ?? null;
    }
  },
  { immediate: true },
);
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/45 px-4 py-6">
      <section
        class="relative box-border flex max-h-[92vh] w-full max-w-5xl flex-col overflow-hidden rounded-xl shadow-2xl"
        :class="isIndoorStep ? 'bg-black text-white' : 'bg-white text-neutral-950'"
      >
        <button
          type="button"
          class="absolute right-6 top-6 z-10 flex h-10 w-10 items-center justify-center text-4xl font-light"
          :class="isIndoorStep ? 'text-white' : 'text-neutral-950'"
          aria-label="Close modal"
          @click="closeModal"
        >
          x
        </button>

        <div class="flex-1 overflow-y-auto px-6 py-8 sm:px-10 lg:px-12">
          <template v-if="step === 1">
            <div class="mx-auto flex w-fit rounded-full bg-white p-1 text-sm font-bold text-neutral-500">
              <button
                type="button"
                class="h-9 rounded-full px-5"
                :class="activeProductType === 'indoor' ? 'bg-blue-600 text-white' : ''"
                @click="selectProductType('indoor')"
              >
                Indoor
              </button>
              <button
                type="button"
                class="h-9 rounded-full px-5"
                :class="activeProductType === 'outdoor' ? 'bg-blue-600 text-white' : ''"
                @click="selectProductType('outdoor')"
              >
                Outdoor
              </button>
            </div>

            <p v-if="loading" class="mt-8 text-neutral-500">Loading LED models...</p>
            <p v-else-if="hasError" class="mt-8 text-red-600">Could not load LED models.</p>

            <div
              v-else-if="selectedModel"
              class="mt-12 flex min-h-[560px] flex-col items-center justify-between text-center"
            >
              <div>
                <h2 class="text-3xl font-black uppercase tracking-normal">
                  {{ selectedModel.name }}
                </h2>
                <p class="mt-1 text-sm" :class="isIndoorStep ? 'text-neutral-200' : 'text-neutral-500'">
                  {{ selectedModel.subtitle }}
                </p>
              </div>

              <div class="relative mt-8 flex w-full items-center justify-center">
                <button
                  type="button"
                  class="absolute left-0 flex h-12 w-12 items-center justify-center rounded-full bg-white/10 text-4xl"
                  :class="isIndoorStep ? 'text-white' : 'bg-neutral-100 text-neutral-950'"
                  @click="selectModelByOffset(-1)"
                >
                  &lt;
                </button>

                <img
                  v-if="selectedModelImage"
                  :src="selectedModelImage"
                  :alt="selectedModel.name"
                  class="h-72 w-full max-w-xl object-contain"
                >
                <div v-else class="h-72 w-full max-w-xl rounded-2xl bg-neutral-100" />

                <button
                  type="button"
                  class="absolute right-0 flex h-12 w-12 items-center justify-center rounded-full bg-white/10 text-4xl"
                  :class="isIndoorStep ? 'text-white' : 'bg-neutral-100 text-neutral-950'"
                  @click="selectModelByOffset(1)"
                >
                  &gt;
                </button>
              </div>

              <div class="mt-10 flex max-w-full items-center gap-4 overflow-x-auto px-8">
                <button
                  v-for="model in activeModels"
                  :key="model.id"
                  type="button"
                  class="h-20 w-24 shrink-0 overflow-hidden rounded border p-2"
                  :class="
                    selectedModel.id === model.id
                      ? 'border-blue-600 bg-blue-50'
                      : isIndoorStep
                        ? 'border-neutral-700 bg-neutral-800'
                        : 'border-neutral-200 bg-neutral-100'
                  "
                  @click="selectModel(model)"
                >
                  <img
                    v-if="resolveLedImage(model.thumbnail_image || model.main_image)"
                    :src="resolveLedImage(model.thumbnail_image || model.main_image)"
                    :alt="model.name"
                    class="h-full w-full object-contain"
                  >
                  <span v-else class="text-xs">{{ model.name }}</span>
                </button>
              </div>
            </div>

            <div v-else class="mt-12 text-center text-neutral-500">
              No {{ activeProductType }} models available.
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
            class="h-11 min-w-36 rounded-full border px-6 text-sm font-semibold disabled:border-neutral-300 disabled:text-neutral-400"
            :class="isIndoorStep ? 'border-white text-white' : 'border-neutral-950 text-neutral-950'"
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
