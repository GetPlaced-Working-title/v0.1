import { create } from "zustand";

interface SearchFilters {
  query: string;
  location: string;
  skills: string[];
  minExperience: number | null;
  employmentType: string;
  workMode: string;
  openToRemote: boolean | null;
}

interface SearchState {
  filters: SearchFilters;
  setFilters: (filters: Partial<SearchFilters>) => void;
  resetFilters: () => void;
}

const defaultFilters: SearchFilters = {
  query: "",
  location: "",
  skills: [],
  minExperience: null,
  employmentType: "",
  workMode: "",
  openToRemote: null,
};

export const useSearchStore = create<SearchState>((set) => ({
  filters: defaultFilters,
  setFilters: (newFilters) =>
    set((state) => ({ filters: { ...state.filters, ...newFilters } })),
  resetFilters: () => set({ filters: defaultFilters }),
}));
