import { apiClient } from "./client";
import type { Company } from "@/lib/types/company";
import type { PaginatedResponse } from "@/lib/types/common";

export const companiesApi = {
  create: (data: Partial<Company>) =>
    apiClient.post<Company>("/companies", data),

  get: (id: string) =>
    apiClient.get<Company>(`/companies/${id}`),

  list: (page = 1, size = 20) =>
    apiClient.get<PaginatedResponse<Company>>("/companies", { params: { page, size } }),

  update: (id: string, data: Partial<Company>) =>
    apiClient.patch<Company>(`/companies/${id}`, data),
};
