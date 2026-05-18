<script setup lang="ts">
import ConfigSidebar from "~/components/configurator/ConfigSidebar.vue";
import ConfiguratorShell from "~/components/configurator/ConfiguratorShell.vue";
import ModelSelectorModal from "~/components/configurator/ModelSelectorModal.vue";
import SpecificationsPanel from "~/components/configurator/SpecificationsPanel.vue";
import WallPreview from "~/components/configurator/WallPreview.vue";
import type { ConfiguratorState, LedModel, LedVariant } from "~/types/led";

const { getLedModels } = useLedApi();
const { resolveLedImage } = useLedImages();

// Django API -> useLedApi -> esta pagina -> modal -> seleccion local -> sidebar/preview.
const { data: ledModels, pending, error } = await getLedModels();

const isModelModalOpen = ref(false);
const config = reactive<ConfiguratorState>({
  wallWidth: 5,
  wallHeight: 3,
  unit: "meters",
  columns: 1,
  rows: 1,
  resolutionMode: null,
  redundancy: "NO",
  contentMode: "default",
  selectedModel: null,
  selectedVariant: null,
  selectedController: null,
  controllerQuantity: 1,
});

const models = computed(() => ledModels.value ?? []);
const modelImageSrc = computed(() =>
  resolveLedImage(config.selectedModel?.main_image || config.selectedModel?.thumbnail_image),
);

const openModelModal = () => {
  isModelModalOpen.value = true;
};

const closeModelModal = () => {
  isModelModalOpen.value = false;
};

const confirmModelSelection = (payload: { model: LedModel; variant: LedVariant }) => {
  config.selectedModel = payload.model;
  config.selectedVariant = payload.variant;
  config.columns = Math.max(1, config.columns);
  config.rows = Math.max(1, config.rows);
  isModelModalOpen.value = false;
};

const resetConfiguration = () => {
  config.wallWidth = 5;
  config.wallHeight = 3;
  config.unit = "meters";
  config.columns = 1;
  config.rows = 1;
  config.resolutionMode = null;
  config.redundancy = "NO";
  config.contentMode = "default";
  config.selectedModel = null;
  config.selectedVariant = null;
  config.selectedController = null;
  config.controllerQuantity = 1;
};
</script>

<template>
  <ConfiguratorShell>
    <WallPreview
      :selected-variant="config.selectedVariant"
      :wall-width="config.wallWidth"
      :wall-height="config.wallHeight"
      :unit="config.unit"
      :columns="config.columns"
      :rows="config.rows"
      :content-mode="config.contentMode"
      @start-config="openModelModal"
      @reset="resetConfiguration"
    />

    <template #sidebar>
      <ConfigSidebar
        :selected-model="config.selectedModel"
        :selected-variant="config.selectedVariant"
        :model-image-src="modelImageSrc"
        :wall-width="config.wallWidth"
        :wall-height="config.wallHeight"
        :unit="config.unit"
        :columns="config.columns"
        :rows="config.rows"
        :resolution-mode="config.resolutionMode"
        :redundancy="config.redundancy"
        :content-mode="config.contentMode"
        @request-model-change="openModelModal"
        @update:wall-width="config.wallWidth = $event"
        @update:wall-height="config.wallHeight = $event"
        @update:unit="config.unit = $event"
        @update:columns="config.columns = $event"
        @update:rows="config.rows = $event"
        @update:resolution-mode="config.resolutionMode = $event"
        @update:redundancy="config.redundancy = $event"
        @update:content-mode="config.contentMode = $event"
      />
    </template>

    <template #bottom>
      <SpecificationsPanel
        :selected-variant="config.selectedVariant"
        :columns="config.columns"
        :rows="config.rows"
        :redundancy="config.redundancy"
      />
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
