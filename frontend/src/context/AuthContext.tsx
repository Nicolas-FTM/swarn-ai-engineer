// Imports
import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import { getUser, login } from '../services/backend/auth.service';
import { AuthState, LoginCredentials, User } from '../types/auth';
import { clearChatSession } from '../hooks/useChatSession';

// Possible Actions for the context
type Action =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_ERROR'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'RESTORE_SESSION'; payload: User };

// Initial State of the Authentication
const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  error: null,
  isLoading: false,
};

// Possible States decided by the actions
function authReducer(state: AuthState, action: Action): AuthState {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, isLoading: true, error: null };
    case 'LOGIN_SUCCESS':
    case 'RESTORE_SESSION':
      return { ...state, isLoading: false, isAuthenticated: true, user: action.payload, error: null };
    case 'LOGIN_ERROR':
      return { ...state, isLoading: false, isAuthenticated: false, user: null, error: action.payload };
    case 'LOGOUT':
      return { ...initialState };
    default:
      return state;
  }
}

// Auth Context Types
interface AuthContextType {
  state: AuthState;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => void;
}

// Creation of the Auth context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider of the Authentication Process
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Restore the session if it has already stored a token (e. g. at the time of refreshing the page)
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;

    getUser()
      .then((user) => {
        localStorage.setItem('user', JSON.stringify(user));
        dispatch({ type: 'RESTORE_SESSION', payload: user });
      })
      .catch(() => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      });
  }, []);

  const login_context = async (credentials: LoginCredentials): Promise<boolean> => {
    dispatch({ type: 'LOGIN_START' });
    try {

      const tokenData = await login(credentials);
      localStorage.setItem('token', tokenData.access_token);

      const user = await getUser();
      localStorage.setItem('user', JSON.stringify(user));

      dispatch({ type: 'LOGIN_SUCCESS', payload: user });
      return true;
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Incorrect User or Password';
      dispatch({ type: 'LOGIN_ERROR', payload: msg });
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    clearChatSession()
    dispatch({ type: 'LOGOUT' });
  };

  return <AuthContext.Provider value={{ state: state, login: login_context, logout: logout }}>{children}</AuthContext.Provider>;
};

// Export of the useAuth Context
export const useAuth = (): AuthContextType => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must use inside of AuthProvider');
  return ctx;
};