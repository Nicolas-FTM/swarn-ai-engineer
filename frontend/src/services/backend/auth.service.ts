import { api } from "./client";
import type { Token, User } from "../../types/auth";

export async function login(credentials: {
  username: string;
  password: string;
}): Promise<Token> {
  const response = await api.post<Token>(
    "/api/frontend/login",
    credentials
  );

  return response.data;
}

export async function getUser(): Promise<User> {
  const response = await api.get<User>("/api/frontend/me");
  return response.data;
}