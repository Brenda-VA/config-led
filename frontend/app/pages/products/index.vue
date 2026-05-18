<script setup lang="ts">
import type { LedModel, LedVariant } from "~/types/led";

const { getLedModels } = useLedApi();
const { resolveLedImage } = useLedImages();

// Django API -> useLedApi -> esta pagina -> modal -> seleccion local -> sidebar/preview.
const { data: ledModels, pending, error } = await getLedModels();

const isModelModalOpen = ref(false);
const selectedModel = ref<LedModel | null>(null);
const selectedVariant = ref<LedVariant | null>(null);

const models = computed(() => ledModels.value ?? []);
const modelImageSrc = computed(() =>
  resolveLedImage(selectedModel.value?.main_image || selectedModel.value?.thumbnail_image),
);

const openModelModal = () => {
  isModelModalOpen.value = true;
};

const closeModelModal = () => {
  isModelModalOpen.value = false;
};

const confirmModelSelection = (payload: { model: LedModel; variant: LedVariant }) => {
  selectedModel.value = payload.model;
  selectedVariant.value = payload.variant;
  isModelModalOpen.value = false;
};

const resetConfiguration = () => {
  selectedModel.value = null;
  selectedVariant.value = null;
};
</script>

<template>
  <ConfiguratorShell>
    <WallPreview
      :selected-variant="selectedVariant"
      @start-config="openModelModal"
      @reset="resetConfiguration"
    />

    <template #sidebar>
      <ConfigSidebar
        :selected-model="selectedModel"
        :selected-variant="selectedVariant"
        :model-image-src="modelImageSrc"
        @change-model="openModelModal"
      />
    </template>

    <template #bottom>
      <SpecificationsPanel :selected-variant="selectedVariant" />
    </template>
  </ConfiguratorShell>

  <ModelSelectorModal
    v-if="isModelModalOpen"
    :models="models"
    :loading="pending"
    :has-error="Boolean(error)"
    @close="closeModelModal"
    @confirm="confirmModelSelection"
  />
</template>
