"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FileUpload } from "@/components/shared/file-upload";

export default function CandidateVideosPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Skill Demonstration Videos</h1>

      <Card>
        <CardHeader>
          <CardTitle>Upload Video</CardTitle>
        </CardHeader>
        <CardContent>
          <FileUpload
            accept="video/mp4,video/webm,video/quicktime"
            onUpload={async (file) => console.log("upload", file)}
            label="Upload Skill Demo Video"
            description="Record yourself explaining a technical concept, solving a problem, or presenting a project. AI will analyze communication, confidence, and technical depth."
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Your Videos</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">No videos uploaded yet.</p>
        </CardContent>
      </Card>
    </div>
  );
}
