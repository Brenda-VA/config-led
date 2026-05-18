<script setup lang="ts">
type Product = {
  id: number;
  name: string;
  product_type: "indoor" | "outdoor";
  cabinet_width_mm: string;
  cabinet_height_mm: string;
  pixel_pitch: string;
  price: string;
  is_active: boolean;
};

const {
  data: products,
  pending,
  error,
} = await useFetch<Product[]>("http://127.0.0.1:8000/api/products/");
</script>

<template>
  <main class="p-8">
    <h1 class="text-3xl font-bold">Configurador LED</h1>

    <p class="mt-2 text-gray-600">Productos cargados desde Django.</p>

    <p v-if="pending" class="mt-6">Cargando productos...</p>

    <p v-else-if="error" class="mt-6 text-red-600">
      Error al cargar productos.
    </p>

    <ul v-else class="mt-6 space-y-4">
      <li
        v-for="product in products"
        :key="product.id"
        class="rounded-xl border p-4"
      >
        <h2 class="text-xl font-semibold">
          {{ product.name }}
        </h2>

        <p>Tipo: {{ product.product_type }}</p>
        <p>
          Cabinet: {{ product.cabinet_width_mm }} x
          {{ product.cabinet_height_mm }} mm
        </p>
        <p>Pixel pitch: {{ product.pixel_pitch }}</p>
        <p>Precio: {{ product.price }} €</p>
      </li>
    </ul>
  </main>
</template>
