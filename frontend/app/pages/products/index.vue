<script setup lang="ts">
type LedModel = {
  id: number;
  name: string;
  slug: string;
  product_type: "indoor" | "outdoor";
  subtitle: string;
  description: string;
  main_image: string;
  thumbnail_image: string;
  variants_count: number;
  is_active: boolean;
  display_order: number;
};

const {
  data: ledModels,
  pending,
  error,
} = await useFetch<LedModel[]>("http://127.0.0.1:8000/api/led-models/");
</script>

<template>
  <main class="p-8">
    <h1 class="text-3xl font-bold">Configurador LED</h1>

    <p class="mt-2 text-gray-600">Modelos LED cargados desde Django.</p>

    <p v-if="pending" class="mt-6">Cargando modelos...</p>

    <p v-else-if="error" class="mt-6 text-red-600">Error al cargar modelos.</p>

    <ul v-else class="mt-6 space-y-4">
      <li
        v-for="model in ledModels"
        :key="model.id"
        class="rounded-xl border p-4"
      >
        <h2 class="text-xl font-semibold">
          {{ model.name }}
        </h2>

        <p>Tipo: {{ model.product_type }}</p>
        <p>{{ model.subtitle }}</p>
        <p>Variantes: {{ model.variants_count }}</p>
        <p>Imagen backend: {{ model.main_image }}</p>
      </li>
    </ul>
  </main>
</template>
