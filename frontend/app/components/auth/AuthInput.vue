<script setup lang="ts">
const model = defineModel<string>({ required: true });

withDefaults(
  defineProps<{
    inputId: string;
    label: string;
    type?: string;
    placeholder?: string;
    autocomplete?: string;
    required?: boolean;
  }>(),
  {
    type: "text",
    placeholder: "",
    autocomplete: "off",
    required: false,
  },
);
</script>

<template>
  <label :for="inputId" class="block text-sm font-medium text-neutral-950">
    {{ label }}
  </label>
  <input
    :id="inputId"
    v-model="model"
    :type="type"
    :placeholder="placeholder"
    :autocomplete="autocomplete"
    :required="required"
    class="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm text-neutral-950 outline-none transition placeholder:text-slate-500 focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20"
  >
</template>
