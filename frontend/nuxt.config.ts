// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  // La app usa frontend/app/pages como router de Nuxt 4.
  // Por ahora las URLs de API estan escritas directamente en las paginas.
  devtools: { enabled: true }
})
