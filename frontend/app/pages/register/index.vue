<script setup lang="ts">
import AuthInput from "~/components/auth/AuthInput.vue";
import AuthLayout from "~/components/auth/AuthLayout.vue";
import { getAuthErrorMessage } from "~/composables/useAuth";
import type { RegisterPayload } from "~/types/auth";

type RegisterForm = {
  email: string;
  firstName: string;
  lastName: string;
  password: string;
  confirmPassword: string;
  company: string;
  country: string;
  phone: string;
  acceptsPrivacy: boolean;
};

const registerForm = reactive<RegisterForm>({
  email: "",
  firstName: "",
  lastName: "",
  password: "",
  confirmPassword: "",
  company: "",
  country: "Spain",
  phone: "",
  acceptsPrivacy: false,
});

const registerMessage = ref("");
const registerError = ref("");
const { register, pending } = useAuth();

const handleRegisterSubmit = async () => {
  registerMessage.value = "";
  registerError.value = "";

  if (!registerForm.acceptsPrivacy) {
    registerError.value = "You need to accept the Privacy Policy to create an account.";
    return;
  }

  const payload: RegisterPayload = {
    email: registerForm.email,
    first_name: registerForm.firstName,
    last_name: registerForm.lastName,
    password: registerForm.password,
    confirm_password: registerForm.confirmPassword,
    company: registerForm.company,
    country: registerForm.country,
    phone: registerForm.phone,
  };

  try {
    await register(payload);
    registerMessage.value = "Account created successfully.";
    await navigateTo("/products");
  } catch (error) {
    registerError.value = getAuthErrorMessage(error);
  }
};
</script>

<template>
  <AuthLayout card-class="max-w-[460px]">
    <form class="space-y-3" @submit.prevent="handleRegisterSubmit">
      <div>
        <h1 class="text-2xl font-black tracking-normal">Create Account</h1>
        <p class="text-sm text-neutral-500">
          Existing account?
          <NuxtLink to="/login" class="font-medium text-purple-800">Sign in</NuxtLink>
        </p>
      </div>

      <AuthInput
        v-model="registerForm.email"
        input-id="register-email"
        label="Email"
        type="email"
        placeholder="Please enter your email"
        autocomplete="email"
        required
      />

      <AuthInput
        v-model="registerForm.firstName"
        input-id="register-first-name"
        label="First Name"
        placeholder="Please enter your first name"
        autocomplete="given-name"
        required
      />

      <AuthInput
        v-model="registerForm.lastName"
        input-id="register-last-name"
        label="Last Name"
        placeholder="Please enter your last name"
        autocomplete="family-name"
        required
      />

      <AuthInput
        v-model="registerForm.password"
        input-id="register-password"
        label="Password"
        type="password"
        placeholder="Password must be at least 8 characters long"
        autocomplete="new-password"
        required
      />

      <AuthInput
        v-model="registerForm.confirmPassword"
        input-id="register-confirm-password"
        label="Confirm Password"
        type="password"
        placeholder="Please enter your password again"
        autocomplete="new-password"
        required
      />

      <AuthInput
        v-model="registerForm.company"
        input-id="register-company"
        label="Company"
        placeholder="Please enter your company name"
        autocomplete="organization"
      />

      <label for="register-country" class="block text-sm font-medium text-neutral-950">
        Country
      </label>
      <select
        id="register-country"
        v-model="registerForm.country"
        class="mt-1 h-10 w-full rounded border border-slate-300 px-3 text-sm text-neutral-950 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-600/20"
      >
        <option>Spain</option>
        <option>France</option>
        <option>Germany</option>
        <option>United Kingdom</option>
        <option>United States</option>
      </select>

      <AuthInput
        v-model="registerForm.phone"
        input-id="register-phone"
        label="Phone (optional)"
        type="tel"
        placeholder="+34  Enter a phone number"
        autocomplete="tel"
      />

      <label class="flex items-start gap-2 pt-2 text-sm text-neutral-950">
        <input v-model="registerForm.acceptsPrivacy" type="checkbox" class="mt-1 h-4 w-4">
        <span>
          By creating an account, you agree to our
          <NuxtLink to="/register" class="text-blue-700 underline">Privacy Policy</NuxtLink>
        </span>
      </label>

      <button
        type="submit"
        class="mt-3 h-12 w-full rounded-full bg-blue-600 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:bg-neutral-300"
        :disabled="pending"
      >
        {{ pending ? "Creating account..." : "Register" }}
      </button>

      <p v-if="registerMessage" class="rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">
        {{ registerMessage }}
      </p>
      <p v-if="registerError" class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
        {{ registerError }}
      </p>
    </form>
  </AuthLayout>
</template>
