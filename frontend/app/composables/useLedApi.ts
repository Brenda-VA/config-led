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
  const { getCsrfHeaders } = useAuth();

  const getServerCookieHeaders = () => {
    return import.meta.server ? useRequestHeaders(["cookie"]) : undefined;
  };

  const getLedModels = () => {
    return useFetch<LedModel[]>(`${apiBase}/led-models/`, {
      credentials: "include",
      headers: getServerCookieHeaders(),
    });
  };

  const getLedModelDetail = (slug: string) => {
    return useFetch<LedModelDetail>(`${apiBase}/led-models/${slug}/`, {
      credentials: "include",
      headers: getServerCookieHeaders(),
    });
  };

  const fetchLedModelDetail = (slug: string) => {
    return $fetch<LedModelDetail>(`${apiBase}/led-models/${slug}/`, {
      credentials: "include",
    });
  };

  const getControllers = () => {
    return useFetch<LedController[]>(`${apiBase}/controllers/`, {
      credentials: "include",
      headers: getServerCookieHeaders(),
    });
  };

  const saveProject = (payload: SaveProjectPayload) => {
    return $fetch<SavedProjectResponse>(`${apiBase}/projects/`, {
      method: "POST",
      body: payload,
      credentials: "include",
      headers: getCsrfHeaders(),
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
