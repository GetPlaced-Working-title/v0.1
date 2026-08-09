import { create } from "zustand";
import type { Candidate } from "@/lib/types/candidate";

interface CandidateState {
  candidate: Candidate | null;
  setCandidate: (candidate: Candidate | null) => void;
}

export const useCandidateStore = create<CandidateState>((set) => ({
  candidate: null,
  setCandidate: (candidate) => set({ candidate }),
}));
