import { apiClient } from "./client";
import type { Resume } from "@/lib/types/candidate";

export const resumesApi = {
  upload: (candidateId: string, file: File) => {
    const form = new FormData();
    form.append("file", file);
    return apiClient.post<{ id: string; file_url: string; processing_status: string }>(
      `/resumes/upload`,
      form,
      {
        params: { candidate_id: candidateId },
        headers: { "Content-Type": "multipart/form-data" },
      }
    );
  },

  list: (candidateId: string) =>
    apiClient.get<Resume[]>("/resumes", { params: { candidate_id: candidateId } }),

  get: (id: string) =>
    apiClient.get<Resume>(`/resumes/${id}`),
};
