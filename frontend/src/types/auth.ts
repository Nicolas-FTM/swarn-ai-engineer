export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: 'baker' | 'sales' | 'hr' | 'cofounder' | 'admin';
  is_active: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}