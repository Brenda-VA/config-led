// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: "http://127.0.0.1:8000/api",
    },
  },
  compatibilityDate: "2025-07-15",
  // La app usa frontend/app/pages como router de Nuxt 4.
  // Por ahora las URLs de API estan escritas directamente en las paginas.
  devtools: { enabled: true },
});
