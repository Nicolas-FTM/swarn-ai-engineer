import { api } from "../client";
import { clearChatSession } from "../../../hooks/useChatSession";
import type { AxiosError, AxiosResponse } from "axios";

export function setupResponseInterceptor() {
  api.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error: AxiosError) => {
      const status = error.response?.status;

      if (status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        clearChatSession();
        window.location.href = "/login";
      }

      if (status === 403) {
        window.location.href = "/unauthorized";
      }

      return Promise.reject(error);
    }
  );
}