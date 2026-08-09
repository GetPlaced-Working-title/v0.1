"use client";

import { useQuery } from "@tanstack/react-query";
import { jobsApi } from "@/lib/api/jobs";

export function useJobs(params?: { company_id?: string; page?: number; size?: number }) {
  return useQuery({
    queryKey: ["jobs", params],
    queryFn: () => jobsApi.list(params).then((r) => r.data),
  });
}

export function useJob(id: string) {
  return useQuery({
    queryKey: ["job", id],
    queryFn: () => jobsApi.get(id).then((r) => r.data),
    enabled: !!id,
  });
}
