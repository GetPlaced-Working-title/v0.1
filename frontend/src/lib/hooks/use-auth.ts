"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/lib/stores/auth-store";
import { apiClient } from "@/lib/api/client";

export function useAuth() {
  const { user, isLoading, setUser, setLoading } = useAuthStore();

  useEffect(() => {
    async function fetchUser() {
      try {
        setLoading(true);
        const { data } = await apiClient.get("/auth/me");
        setUser(data);
      } catch {
        setUser(null);
      }
    }
    fetchUser();
  }, [setUser, setLoading]);

  return { user, isLoading };
}
