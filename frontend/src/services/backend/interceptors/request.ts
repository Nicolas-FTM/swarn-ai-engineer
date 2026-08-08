import { api } from "../client";
import type { InternalAxiosRequestConfig, AxiosError } from "axios";

export function setupRequestInterceptor() {
  api.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      const token = localStorage.getItem("token");

      if (token) {
        config.headers.set("Authorization", `Bearer ${token}`);
      }

      return config;
    },
    (error: AxiosError) => Promise.reject(error)
  );
}