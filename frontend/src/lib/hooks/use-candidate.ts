"use client";

import { useQuery } from "@tanstack/react-query";
import { candidatesApi } from "@/lib/api/candidates";

export function useCandidate(id: string) {
  return useQuery({
    queryKey: ["candidate", id],
    queryFn: () => candidatesApi.get(id).then((r) => r.data),
    enabled: !!id,
  });
}

export function useCandidateSkills(candidateId: string) {
  return useQuery({
    queryKey: ["candidate", candidateId, "skills"],
    queryFn: () => candidatesApi.listSkills(candidateId).then((r) => r.data),
    enabled: !!candidateId,
  });
}

export function useCandidateProjects(candidateId: string) {
  return useQuery({
    queryKey: ["candidate", candidateId, "projects"],
    queryFn: () => candidatesApi.listProjects(candidateId).then((r) => r.data),
    enabled: !!candidateId,
  });
}
