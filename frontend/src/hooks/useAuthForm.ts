// Imports
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

// Classes for the form
interface FormData {
  username: string;
  password: string;
}
interface FormErrors {
  username?: string;
  password?: string;
}

// Export of the useAuth Context
export function useAuthForm() {
  const { login } = useAuth();
  const [formData, setFormData] = useState<FormData>({ username: '', password: '' });
  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const validate = (): boolean => {
    const newErrors: FormErrors = {};
    if (!formData.username.trim()) newErrors.username = 'El usuario es obligatorio';
    if (!formData.password) newErrors.password = 'La contraseña es obligatoria';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    await login(formData);
    setIsLoading(false);
    // Login.tsx redirige a /chat al detectar state.isAuthenticated
  };

  return { formData, errors, isLoading, handleChange, handleSubmit };
}