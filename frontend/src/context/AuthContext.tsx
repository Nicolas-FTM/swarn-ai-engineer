import React, { createContext, useContext, useEffect, useState } from 'react';
import { AuthState, LoginData } from '../types/auth';
import { apiService } from '../services/api';

// Create AuthContext with default values
const AuthContext = createContext<{
  state: AuthState;
  login: (credentials: LoginData) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}>({
  state: {
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
  },
  login: async () => {},
  logout: () => {},
  checkAuth: async () => {},
});

// AuthProvider component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    isLoading: false,
    error: null,
  });

  // Check authentication status on component mount
  useEffect(() => {
    checkAuth();
  }, []);

  const login = async (credentials: LoginData) => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      const tokenData = await apiService.login(credentials);
      // Store token and user info
      localStorage.setItem('token', tokenData.access_token);

      // Fetch user info
      const user = await apiService.getUser();
      localStorage.setItem('user', JSON.stringify(user));

      setState({
        user,
        token: tokenData.access_token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Login failed';
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,
    });
  };

  const checkAuth = async () => {
    if (!state.token) return;

    setState(prev => ({ ...prev, isLoading: true }));

    try {
      const user = await apiService.getUser();
      localStorage.setItem('user', JSON.stringify(user));
      setState(prev => ({
        ...prev,
        user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      }));
    } catch (error) {
      logout();
    }
  };

  const value = {
    state,
    login,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook for using auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
