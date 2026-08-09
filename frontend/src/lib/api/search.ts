import { apiClient } from "./client";

export const searchApi = {
  searchCandidates: (data: {
    query?: string;
    location?: string;
    skills?: string[];
    min_experience?: number;
    open_to_remote?: boolean;
    page?: number;
    size?: number;
  }) => apiClient.post("/search/candidates", data),

  searchJobs: (data: {
    query?: string;
    location?: string;
    employment_type?: string;
    work_mode?: string;
    skills?: string[];
    page?: number;
    size?: number;
  }) => apiClient.post("/search/jobs", data),
};
