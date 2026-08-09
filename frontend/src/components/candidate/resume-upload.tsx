"use client";

import { useState } from "react";
import { FileUpload } from "@/components/shared/file-upload";
import { resumesApi } from "@/lib/api/resumes";
import { useQueryClient } from "@tanstack/react-query";

interface ResumeUploadProps {
  candidateId: string;
}

export function ResumeUpload({ candidateId }: ResumeUploadProps) {
  const [status, setStatus] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const handleUpload = async (file: File) => {
    setStatus("Uploading...");
    try {
      const { data } = await resumesApi.upload(candidateId, file);
      setStatus(`Upload complete. Status: ${data.processing_status}`);
      queryClient.invalidateQueries({ queryKey: ["candidate", candidateId, "resumes"] });
    } catch (err) {
      setStatus("Upload failed. Please try again.");
    }
  };

  return (
    <div className="space-y-3">
      <FileUpload
        accept=".pdf,.doc,.docx"
        onUpload={handleUpload}
        label="Upload Resume"
        description="PDF or Word document. AI will extract and analyze all content."
      />
      {status && (
        <p className="text-sm text-center text-muted-foreground">{status}</p>
      )}
    </div>
  );
}
