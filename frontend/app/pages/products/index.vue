<script setup lang="ts">
import ConfigSidebar from "~/components/configurator/ConfigSidebar.vue";
import ConfiguratorShell from "~/components/configurator/ConfiguratorShell.vue";
import ModelSelectorModal from "~/components/configurator/ModelSelectorModal.vue";
import SpecificationsPanel from "~/components/configurator/SpecificationsPanel.vue";
import WallPreview from "~/components/configurator/WallPreview.vue";
import type {
  BackendContentMode,
  BackendRedundancyMode,
  BackendUnit,
  ConfiguratorState,
  ContentMode,
  LedModel,
  LedVariant,
  RedundancyMode,
  SaveProjectPayload,
} from "~/types/led";

const { getLedModels, getControllers, saveProject } = useLedApi();
const { resolveLedImage } = useLedImages();
const { isAuthenticated } = useAuth();

// Esta pagina es la dueña del estado: sidebar, preview y specs leen de aqui.
const { data: ledModels, pending, error } = await getLedModels();
const {
  data: controllers,
  pending: controllersPending,
  error: controllersError,
} = await getControllers();

const isModelModalOpen = ref(false);
const saveStatus = ref<"idle" | "saving" | "success" | "error">("idle");
const saveMessage = ref("");
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
const controllerOptions = computed(() => controllers.value ?? []);
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
  saveStatus.value = "idle";
  saveMessage.value = "";
};

const toMeters = (value: number) => {
  return config.unit === "feet" ? value * 0.3048 : value;
};

const unitMap: Record<ConfiguratorState["unit"], BackendUnit> = {
  meters: "m",
  feet: "ft",
};

const redundancyMap: Record<RedundancyMode, BackendRedundancyMode> = {
  NO: "none",
  POWER: "power",
  DATA: "data",
};

const contentModeMap: Record<ContentMode, BackendContentMode> = {
  default: "default_image",
  preview: "preview_video",
  upload: "upload_image",
  none: "no_image",
};

type ApiErrorLike = {
  response?: {
    status?: number;
  };
  status?: number;
  message?: string;
};

const getApiErrorStatus = (error: unknown) => {
  if (typeof error !== "object" || error === null) {
    return undefined;
  }

  const apiError = error as ApiErrorLike;
  return apiError.response?.status ?? apiError.status;
};

const buildProjectPayload = (): SaveProjectPayload | null => {
  if (!config.selectedVariant) {
    return null;
  }

  const projectModelName = config.selectedModel?.name ?? "LED";
  const projectVariantName = config.selectedVariant.model_name;

  return {
    name: `${projectModelName} - ${projectVariantName}`,
    selected_variant: config.selectedVariant.id,
    controller: config.selectedController?.id ?? null,
    wall_width_m: toMeters(config.wallWidth).toFixed(2),
    wall_height_m: toMeters(config.wallHeight).toFixed(2),
    columns: config.columns,
    rows: config.rows,
    unit: unitMap[config.unit],
    resolution_preset: config.resolutionMode ?? "",
    redundancy: redundancyMap[config.redundancy],
    content_mode: contentModeMap[config.contentMode],
    custom_image_path: "",
  };
};

const handleExportPdfClick = async () => {
  // De momento este boton guarda el proyecto; luego aqui enganchamos jsPDF.
  const payload = buildProjectPayload();

  if (!payload) {
    saveStatus.value = "error";
    saveMessage.value = "Selecciona un modelo y una variante antes de guardar.";
    return;
  }

  // Si el usuario no esta autenticado, el backend bloqueara igualmente el guardado.
  if (!isAuthenticated.value) {
    saveStatus.value = "error";
    saveMessage.value = "Debes iniciar sesión para guardar el proyecto.";
    return;
  }

  saveStatus.value = "saving";
  saveMessage.value = "";

  try {
    await saveProject(payload);
    saveStatus.value = "success";
    saveMessage.value = "Proyecto guardado correctamente.";
  } catch (error) {
    const status = getApiErrorStatus(error);

    saveStatus.value = "error";
    saveMessage.value =
      status === 401 || status === 403
        ? "Debes iniciar sesión para guardar el proyecto."
        : "No se pudo guardar el proyecto. Revisa los datos e inténtalo de nuevo.";
  }
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
        :controllers="controllerOptions"
        :controllers-loading="controllersPending"
        :controllers-error="Boolean(controllersError)"
        :selected-controller="config.selectedController"
        :controller-quantity="config.controllerQuantity"
        :save-status="saveStatus"
        :save-message="saveMessage"
        @request-model-change="openModelModal"
        @update:wall-width="config.wallWidth = $event"
        @update:wall-height="config.wallHeight = $event"
        @update:unit="config.unit = $event"
        @update:columns="config.columns = $event"
        @update:rows="config.rows = $event"
        @update:resolution-mode="config.resolutionMode = $event"
        @update:redundancy="config.redundancy = $event"
        @update:content-mode="config.contentMode = $event"
        @update:selected-controller="config.selectedController = $event"
        @update:controller-quantity="config.controllerQuantity = $event"
        @export-pdf="handleExportPdfClick"
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
