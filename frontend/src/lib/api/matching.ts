import { apiClient } from "./client";
import type { JobMatch } from "@/lib/types/job";
import type { PaginatedResponse } from "@/lib/types/common";

export const matchingApi = {
  runMatch: (jobId: string, topK = 10) =>
    apiClient.post("/matching/run", { job_id: jobId, top_k: topK }),

  getJobMatches: (jobId: string, page = 1, size = 20) =>
    apiClient.get<PaginatedResponse<JobMatch>>(`/matching/jobs/${jobId}`, {
      params: { page, size },
    }),

  updateMatchStatus: (matchId: string, status: string, notes?: string) =>
    apiClient.patch<JobMatch>(`/matching/matches/${matchId}`, {
      status,
      recruiter_notes: notes,
    }),
};
