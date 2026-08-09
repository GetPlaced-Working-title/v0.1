"use client";

import { useCallback, useId, useState } from "react";
import { Button } from "@/components/ui/button";

interface FileUploadProps {
  accept?: string;
  onUpload: (file: File) => Promise<void>;
  label?: string;
  description?: string;
}

export function FileUpload({ accept, onUpload, label = "Upload File", description }: FileUploadProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const inputId = useId();

  const handleFile = useCallback(
    async (file: File) => {
      setIsUploading(true);
      try {
        await onUpload(file);
      } finally {
        setIsUploading(false);
      }
    },
    [onUpload]
  );

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label={label}
      className={`flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-8 transition-colors ${
        dragOver ? "border-primary bg-primary/5" : "border-muted-foreground/25"
      }`}
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={(e) => {
        e.preventDefault();
        setDragOver(false);
        const file = e.dataTransfer.files[0];
        if (file) handleFile(file);
      }}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          document.getElementById(inputId)?.click();
        }
      }}
    >
      <p className="mb-2 text-sm font-medium">{label}</p>
      {description && <p className="mb-4 text-xs text-muted-foreground">{description}</p>}
      <input
        type="file"
        accept={accept}
        className="hidden"
        id={inputId}
        aria-label={label}
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
        }}
      />
      <label htmlFor={inputId}>
        <Button variant="outline" disabled={isUploading} asChild>
          <span>{isUploading ? "Uploading..." : "Choose File"}</span>
        </Button>
      </label>
    </div>
  );
}
