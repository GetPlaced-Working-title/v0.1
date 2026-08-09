import { apiClient } from "./client";
import type { Job, JobMatch } from "@/lib/types/job";
import type { PaginatedResponse } from "@/lib/types/common";

export const jobsApi = {
  create: (companyId: string, data: Partial<Job>) =>
    apiClient.post<Job>(`/jobs`, data, { params: { company_id: companyId } }),

  get: (id: string) =>
    apiClient.get<Job>(`/jobs/${id}`),

  list: (params?: { company_id?: string; status?: string; page?: number; size?: number }) =>
    apiClient.get<PaginatedResponse<Job>>("/jobs", { params }),

  update: (id: string, data: Partial<Job>) =>
    apiClient.patch<Job>(`/jobs/${id}`, data),

  publish: (id: string) =>
    apiClient.post<Job>(`/jobs/${id}/publish`),

  close: (id: string) =>
    apiClient.post<Job>(`/jobs/${id}/close`),

  search: (params: {
    query?: string;
    location?: string;
    employment_type?: string;
    work_mode?: string;
    page?: number;
    size?: number;
  }) => apiClient.get<PaginatedResponse<Job>>("/jobs/search", { params }),
};
