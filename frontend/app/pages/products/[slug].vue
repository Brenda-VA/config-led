<script setup lang="ts">
const route = useRoute();
const slug = String(route.params.slug);

const { getLedModelDetail } = useLedApi();

const { data: model, pending, error } = await getLedModelDetail(slug);
</script>

<template>
  <main class="p-8">
    <NuxtLink to="/products"> ← Volver </NuxtLink>

    <p v-if="pending" class="mt-6">Cargando modelo...</p>

    <p v-else-if="error" class="mt-6 text-red-600">
      Error al cargar el modelo.
    </p>

    <section v-else-if="model" class="mt-6">
      <h1 class="text-3xl font-bold">
        {{ model.name }}
      </h1>

      <p class="mt-2 text-gray-600">
        {{ model.subtitle }}
      </p>

      <table class="mt-8 w-full border-collapse">
        <thead>
          <tr>
            <th class="border p-2">Model Name</th>
            <th class="border p-2">Pixel Pitch</th>
            <th class="border p-2">Brightness</th>
            <th class="border p-2">Dimensions</th>
            <th class="border p-2">Refresh Rate</th>
            <th class="border p-2">Web Price / Cabinet</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="variant in model.variants" :key="variant.id">
            <td class="border p-2">{{ variant.model_name }}</td>
            <td class="border p-2">{{ variant.pixel_pitch }} mm</td>
            <td class="border p-2">{{ variant.brightness_nits }} nits</td>
            <td class="border p-2">
              {{ variant.cabinet_width_mm }} x {{ variant.cabinet_height_mm }} x
              {{ variant.cabinet_depth_mm }} mm
            </td>
            <td class="border p-2">{{ variant.refresh_rate_hz }} Hz</td>
            <td class="border p-2">
              {{ variant.web_price_per_cabinet ?? "-" }}
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>
