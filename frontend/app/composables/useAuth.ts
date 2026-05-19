import type { AuthResponse, AuthUser, LoginPayload, RegisterPayload } from "~/types/auth";

type ApiErrorPayload = {
  detail?: string;
  non_field_errors?: string[];
  email?: string[];
  password?: string[];
  confirm_password?: string[];
};

type ApiErrorLike = {
  data?: ApiErrorPayload;
  response?: {
    status?: number;
    _data?: ApiErrorPayload;
  };
  message?: string;
};

const readBrowserCookie = (name: string) => {
  if (import.meta.server) {
    return "";
  }

  const cookie = document.cookie
    .split("; ")
    .find((item) => item.startsWith(`${encodeURIComponent(name)}=`));

  return cookie ? decodeURIComponent(cookie.split("=").slice(1).join("=")) : "";
};

export const getAuthErrorMessage = (error: unknown) => {
  if (typeof error !== "object" || error === null) {
    return "Something went wrong. Please try again.";
  }

  const apiError = error as ApiErrorLike;
  const data = apiError.data ?? apiError.response?._data;

  if (data?.detail) {
    return data.detail;
  }
  if (data?.non_field_errors?.length) {
    return data.non_field_errors[0];
  }
  if (data?.email?.length) {
    return data.email[0];
  }
  if (data?.password?.length) {
    return data.password[0];
  }
  if (data?.confirm_password?.length) {
    return data.confirm_password[0];
  }

  return apiError.message ?? "Something went wrong. Please try again.";
};

export const useAuth = () => {
  // Este composable centraliza toda la autenticacion para no repetir logica.
  const config = useRuntimeConfig();
  const authBase = config.public.authBase;
  const user = useState<AuthUser | null>("auth:user", () => null);
  const csrfToken = useState("auth:csrfToken", () => "");
  const pending = useState("auth:pending", () => false);

  const isAuthenticated = computed(() => Boolean(user.value));

  const getServerCookieHeaders = () => {
    return import.meta.server ? useRequestHeaders(["cookie"]) : undefined;
  };

  const getCsrfHeaders = () => {
    const token = csrfToken.value || readBrowserCookie("csrftoken");
    return token ? { "X-CSRFToken": token } : {};
  };

  const fetchCurrentUser = async () => {
    try {
      const response = await $fetch<AuthResponse>(`${authBase}/me/`, {
        credentials: "include",
        headers: getServerCookieHeaders(),
      });

      user.value = response.user;
      csrfToken.value = response.csrf_token;
      return response.user;
    } catch {
      user.value = null;
      return null;
    }
  };

  const login = async (payload: LoginPayload) => {
    pending.value = true;

    try {
      const response = await $fetch<AuthResponse>(`${authBase}/login/`, {
        method: "POST",
        body: payload,
        credentials: "include",
        headers: getCsrfHeaders(),
      });

      user.value = response.user;
      csrfToken.value = response.csrf_token;
      return response.user;
    } finally {
      pending.value = false;
    }
  };

  const register = async (payload: RegisterPayload) => {
    pending.value = true;

    try {
      const response = await $fetch<AuthResponse>(`${authBase}/register/`, {
        method: "POST",
        body: payload,
        credentials: "include",
        headers: getCsrfHeaders(),
      });

      user.value = response.user;
      csrfToken.value = response.csrf_token;
      return response.user;
    } finally {
      pending.value = false;
    }
  };

  const logout = async () => {
    pending.value = true;

    try {
      await $fetch(`${authBase}/logout/`, {
        method: "POST",
        credentials: "include",
        headers: getCsrfHeaders(),
      });
    } finally {
      user.value = null;
      csrfToken.value = "";
      pending.value = false;
    }
  };

  return {
    user,
    csrfToken,
    pending,
    isAuthenticated,
    getCsrfHeaders,
    fetchCurrentUser,
    login,
    register,
    logout,
  };
};
