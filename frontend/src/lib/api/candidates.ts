import { apiClient } from "./client";
import type { Candidate, Project, WorkHistory, Skill, Certificate } from "@/lib/types/candidate";
import type { PaginatedResponse } from "@/lib/types/common";

export const candidatesApi = {
  create: (data: Partial<Candidate>) =>
    apiClient.post<Candidate>("/candidates", data),

  get: (id: string) =>
    apiClient.get<Candidate>(`/candidates/${id}`),

  list: (page = 1, size = 20) =>
    apiClient.get<PaginatedResponse<Candidate>>("/candidates", { params: { page, size } }),

  update: (id: string, data: Partial<Candidate>) =>
    apiClient.patch<Candidate>(`/candidates/${id}`, data),

  search: (params: {
    query?: string;
    location?: string;
    min_experience?: number;
    open_to_remote?: boolean;
    page?: number;
    size?: number;
  }) => apiClient.get<PaginatedResponse<Candidate>>("/candidates/search", { params }),

  addProject: (candidateId: string, data: Partial<Project>) =>
    apiClient.post<Project>(`/candidates/${candidateId}/projects`, data),

  listProjects: (candidateId: string) =>
    apiClient.get<Project[]>(`/candidates/${candidateId}/projects`),

  addWorkHistory: (candidateId: string, data: Partial<WorkHistory>) =>
    apiClient.post<WorkHistory>(`/candidates/${candidateId}/work-history`, data),

  listWorkHistory: (candidateId: string) =>
    apiClient.get<WorkHistory[]>(`/candidates/${candidateId}/work-history`),

  listSkills: (candidateId: string) =>
    apiClient.get<Skill[]>(`/candidates/${candidateId}/skills`),
};
