import { setupRequestInterceptor } from "./interceptors/request";
import { setupResponseInterceptor } from "./interceptors/response";

export function initApi() {
  setupRequestInterceptor();
  setupResponseInterceptor();
}