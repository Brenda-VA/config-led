import type {
  LedController,
  LedModel,
  LedModelDetail,
  SavedProjectResponse,
  SaveProjectPayload,
} from "~/types/led";

// Todas las llamadas a Django viven aqui para no repetir URLs por la app.
export const useLedApi = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  const getLedModels = () => {
    return useFetch<LedModel[]>(`${apiBase}/led-models/`);
  };

  const getLedModelDetail = (slug: string) => {
    return useFetch<LedModelDetail>(`${apiBase}/led-models/${slug}/`);
  };

  const fetchLedModelDetail = (slug: string) => {
    return $fetch<LedModelDetail>(`${apiBase}/led-models/${slug}/`);
  };

  const getControllers = () => {
    return useFetch<LedController[]>(`${apiBase}/controllers/`);
  };

  const saveProject = (payload: SaveProjectPayload) => {
    return $fetch<SavedProjectResponse>(`${apiBase}/projects/`, {
      method: "POST",
      body: payload,
      credentials: "include",
    });
  };

  return {
    getLedModels,
    getLedModelDetail,
    fetchLedModelDetail,
    getControllers,
    saveProject,
  };
};
