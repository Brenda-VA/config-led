export type AuthUser = {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  is_superuser: boolean;
  can_view_prices: boolean;
  company: string;
  country: string;
  phone: string;
};

export type AuthResponse = {
  user: AuthUser | null;
  csrf_token: string;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type RegisterPayload = {
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  confirm_password: string;
  company?: string;
  country?: string;
  phone?: string;
};
