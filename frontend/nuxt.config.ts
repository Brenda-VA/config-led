// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: "http://127.0.0.1:8000/api",
      authBase: "http://127.0.0.1:8000/auth",
    },
  },
  compatibilityDate: "2025-07-15",
  // La app usa frontend/app/pages como router de Nuxt 4.
  // Por ahora las URLs de API estan escritas directamente en las paginas.
  css: ["~/assets/css/main.css"],
  devtools: { enabled: true },
  vite: {
    plugins: [tailwindcss()],
  },
});
