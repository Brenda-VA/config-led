<script setup lang="ts">
import authBackgroundSrc from "../../../assets/recursos/preview-imagen.png";

withDefaults(
  defineProps<{
    cardClass?: string;
  }>(),
  {
    cardClass: "",
  },
);
</script>

<template>
  <main class="relative min-h-screen overflow-hidden bg-black text-white">
    <img
      :src="authBackgroundSrc"
      alt=""
      class="absolute inset-0 h-full w-full scale-110 object-cover opacity-70"
    >
    <div class="absolute inset-0 bg-black/65" />

    <NuxtLink
      to="/products"
      class="absolute left-6 top-6 z-10 text-3xl font-black tracking-normal text-white sm:left-10 sm:top-8"
    >
      RGBs
    </NuxtLink>

    <section
      class="relative z-10 grid min-h-screen grid-cols-1 items-center gap-10 px-6 py-24 sm:px-10 lg:grid-cols-[minmax(0,1fr)_420px] lg:px-32"
    >
      <div class="text-center lg:text-left">
        <p class="text-5xl font-black leading-none tracking-normal sm:text-6xl">BETTER</p>
        <p class="mt-2 text-4xl font-medium leading-none tracking-normal sm:text-5xl">
          visual experience
        </p>
      </div>

      <section
        class="mx-auto w-full rounded-2xl bg-white p-8 text-neutral-950 shadow-2xl sm:p-10"
        :class="cardClass"
      >
        <slot />
      </section>
    </section>
  </main>
</template>
