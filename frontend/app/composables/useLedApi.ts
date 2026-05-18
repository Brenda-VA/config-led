import type { LedModel, LedModelDetail } from "~/types/led";
//esto evita repetir http://127.0.0.1:8000/api
export const useLedApi = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  const getLedModels = () => {
    return useFetch<LedModel[]>(`${apiBase}/led-models/`);
  };

  const getLedModelDetail = (slug: string) => {
    return useFetch<LedModelDetail>(`${apiBase}/led-models/${slug}/`);
  };

  return {
    getLedModels,
    getLedModelDetail,
  };
};
