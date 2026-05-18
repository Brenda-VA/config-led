<script setup lang="ts">
import AuthInput from "~/components/auth/AuthInput.vue";
import AuthLayout from "~/components/auth/AuthLayout.vue";

type LoginForm = {
  email: string;
  password: string;
  rememberMe: boolean;
};

const loginForm = reactive<LoginForm>({
  email: "",
  password: "",
  rememberMe: false,
});

const loginMessage = ref("");

const handleLoginSubmit = () => {
  // Solo UI por ahora; despues conectamos este submit con Django.
  loginMessage.value = "Login form ready. Backend connection pending.";
};
</script>

<template>
  <AuthLayout>
    <form class="space-y-5" @submit.prevent="handleLoginSubmit">
      <div>
        <h1 class="text-2xl font-black tracking-normal">Welcome to login</h1>
      </div>

      <div class="space-y-3">
        <AuthInput
          v-model="loginForm.email"
          input-id="login-email"
          label="Email"
          type="email"
          placeholder="john@doe.com"
          autocomplete="email"
          required
        />

        <AuthInput
          v-model="loginForm.password"
          input-id="login-password"
          label="Password"
          type="password"
          placeholder="********"
          autocomplete="current-password"
          required
        />
      </div>

      <div class="flex flex-col gap-3 text-sm sm:flex-row sm:items-center sm:justify-between">
        <label class="flex items-center gap-2 text-neutral-700">
          <input v-model="loginForm.rememberMe" type="checkbox" class="h-4 w-4">
          Remember me
        </label>

        <NuxtLink to="/login" class="font-medium text-blue-700">
          Forgot your password? ↗
        </NuxtLink>
      </div>

      <button
        type="submit"
        class="h-12 w-full rounded-full bg-blue-600 text-sm font-semibold text-white transition hover:bg-blue-700"
      >
        Sign in
      </button>

      <p v-if="loginMessage" class="rounded-lg bg-blue-50 px-3 py-2 text-sm text-blue-700">
        {{ loginMessage }}
      </p>

      <p class="text-center text-sm text-neutral-950">
        Don't have an account yet?
        <NuxtLink to="/register" class="font-medium text-purple-800">New Account</NuxtLink>
      </p>
    </form>
  </AuthLayout>
</template>
