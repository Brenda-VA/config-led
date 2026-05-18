<script setup lang="ts">
type ProductVariant = {
  id: number;
  model_name: string;
  pixel_pitch: string;
  brightness_nits: number;
  cabinet_width_mm: string;
  cabinet_height_mm: string;
  cabinet_depth_mm: string | null;
  refresh_rate_hz: number;
  web_price_per_cabinet: string | null;
};

type ProductFamilyDetail = {
  id: number;
  name: string;
  slug: string;
  product_type: "indoor" | "outdoor";
  subtitle: string;
  description: string;
  main_image: string;
  thumbnail_image: string;
  variants: ProductVariant[];
};

const route = useRoute();

const {
  data: model,
  pending,
  error,
} = await useFetch<ProductFamilyDetail>(
  `http://127.0.0.1:8000/api/led-models/${route.params.slug}/`,
);
</script>

<template>
  <main class="p-8">
    <NuxtLink to="/products" class="text-blue-600"> ← Volver </NuxtLink>

    <p v-if="pending" class="mt-6">Cargando modelo...</p>

    <p v-else-if="error" class="mt-6 text-red-600">
      Error al cargar el modelo.
    </p>

    <section v-else-if="model" class="mt-6">
      <p class="text-sm uppercase text-gray-500">
        {{ model.product_type }}
      </p>

      <h1 class="text-3xl font-bold">
        {{ model.name }}
      </h1>

      <p class="mt-2 text-gray-600">
        {{ model.description }}
      </p>

      <div class="mt-8 overflow-x-auto">
        <table class="w-full border-collapse text-left">
          <thead>
            <tr class="bg-blue-600 text-white">
              <th class="p-3">Model Name</th>
              <th class="p-3">Pixel Pitch</th>
              <th class="p-3">Brightness</th>
              <th class="p-3">Dimensions</th>
              <th class="p-3">Refresh Rate</th>
              <th class="p-3">Web Price / Cabinet</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="variant in model.variants"
              :key="variant.id"
              class="border-b"
            >
              <td class="p-3">
                {{ variant.model_name }}
              </td>

              <td class="p-3">{{ variant.pixel_pitch }} mm</td>

              <td class="p-3">{{ variant.brightness_nits }} nits</td>

              <td class="p-3">
                {{ variant.cabinet_width_mm }} x
                {{ variant.cabinet_height_mm }} x
                {{ variant.cabinet_depth_mm }} mm
              </td>

              <td class="p-3">{{ variant.refresh_rate_hz }} Hz</td>

              <td class="p-3">
                {{ variant.web_price_per_cabinet ?? "-" }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>
</template>
