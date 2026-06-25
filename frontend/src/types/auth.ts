// ========================
// Domain Entities
// ========================

/**
 * Represents the authenticated user (BackEnd), structure of the response of the backend in Get /auth/me
 * response of the backend in Get /auth/me
 */
export interface User {
  id: string;
  username: string;
  email: string;
  role: 'baker' | 'sales' | 'hr' | 'cofounder' | 'admin';
}

/**
 * Backend Answer at the login (POST /auth/login)
 */
export interface Token {
  access_token: string;
  token_type: string; // usually "bearer"
}

// ========================
// Petition Payloads
// ========================

/**
 * Sent data to backend to login
 */
export interface LoginCredentials {
  username: string;
  password: string;
}

/**
 * If in the future, we add the user register
 */
export interface RegisterCredentials {
  username: string;
  password: string;
  email?: string;
}

// ========================
// Form (useAuthForm)
// ========================

/**
 * Form State of the component login
 */
export interface AuthFormData {
  username: string;
  password: string;
}

/**
 * Validation errors per field
 */
export interface AuthFormErrors {
  username?: string;
  password?: string;
}

// ========================
// Global State (AuthContext)
// ========================

/**
 * Global State of Authentication managing by the reducer
 * in AuthContext.tsx
 */
export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  error: string | null;
  isLoading: boolean;
}

/**
 * Actions that the AuthContext reducer can dispatch
 */
export type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_ERROR'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'RESTORE_SESSION'; payload: User };

/**
 * Context form exposed by useAuth()
 */
export interface AuthContextType {
  state: AuthState;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => void;
}

// ========================
// API Errors (optional, useful to type axios errors
// ========================

/**
 * Typical error form that returns FastAPI:
 * { "detail": "error log" }
 */
export interface ApiErrorResponse {
  detail: string;
}