<template>
  <div class="min-h-screen bg-neutral-100 text-neutral-950">
    <header
      class="relative box-border w-full bg-white flex items-center justify-between gap-4 px-4 py-5 shadow-sm sm:px-6 lg:px-8"
    >
      <NuxtLink to="/products" class="text-xl font-black tracking-normal sm:text-2xl">
        RGBs Display Configurator
      </NuxtLink>

      <div class="flex items-center gap-3">
        <NuxtLink
          to="/login"
          class="flex h-10 items-center rounded-full border border-blue-600 px-5 text-sm font-semibold text-blue-700"
        >
          Sign in
        </NuxtLink>
        <NuxtLink
          to="/register"
          class="flex h-10 items-center rounded-full bg-blue-600 px-5 text-sm font-semibold text-white shadow-sm"
        >
          Register
        </NuxtLink>
      </div>
    </header>

    <main
      class="box-border grid min-h-[calc(100vh-80px)] w-full grid-cols-1 gap-5 p-4 lg:grid-cols-[minmax(0,1fr)_360px] lg:p-8"
    >
      <section
        class="relative box-border min-h-[520px] w-full rounded-2xl border border-neutral-200 bg-neutral-50 p-4 sm:p-6 lg:p-8"
      >
        <slot />
      </section>

      <aside class="w-full lg:sticky lg:top-6 lg:self-start">
        <slot name="sidebar" />
      </aside>
    </main>

    <section class="box-border w-full px-4 pb-8 lg:px-8">
      <slot name="bottom" />
    </section>
  </div>
</template>
