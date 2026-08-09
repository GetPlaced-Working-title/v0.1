"use client";

import { useQuery } from "@tanstack/react-query";
import { searchApi } from "@/lib/api/search";
import { matchingApi } from "@/lib/api/matching";

export function useSearchCandidates(params: Record<string, unknown>) {
  return useQuery({
    queryKey: ["search", "candidates", params],
    queryFn: () => searchApi.searchCandidates(params as any).then((r) => r.data),
  });
}

export function useSearchJobs(params: Record<string, unknown>) {
  return useQuery({
    queryKey: ["search", "jobs", params],
    queryFn: () => searchApi.searchJobs(params as any).then((r) => r.data),
  });
}

export function useJobMatches(jobId: string, page = 1, size = 20) {
  return useQuery({
    queryKey: ["matches", jobId, page, size],
    queryFn: () => matchingApi.getJobMatches(jobId, page, size).then((r) => r.data),
    enabled: !!jobId,
  });
}
