<script setup lang="ts">
const { fetchCurrentUser } = useAuth();

await fetchCurrentUser();
</script>

<template>
  <!-- NuxtPage renderiza la pagina segun la ruta: /products, /products/:slug, etc. -->
  <NuxtPage />
</template>
