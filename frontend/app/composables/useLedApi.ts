import type { LedModel, LedModelDetail } from "~/types/led";

// Punto unico para construir URLs contra la API Django.
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

  return {
    getLedModels,
    getLedModelDetail,
    fetchLedModelDetail,
  };
};
