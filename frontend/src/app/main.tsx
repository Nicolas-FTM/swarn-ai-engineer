import React from 'react';
import ReactDOM from 'react-dom/client';
import AppRouter from '../routes/AppRouter';
import { AuthProvider } from '../context/AuthContext';
import '../styles/globals.css';
import { initApi } from "../services/backend";

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element not found');
}

initApi();

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <AuthProvider>
      <AppRouter />
    </AuthProvider>
  </React.StrictMode>
);
