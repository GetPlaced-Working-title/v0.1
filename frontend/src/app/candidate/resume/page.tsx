"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ResumeUpload } from "@/components/candidate/resume-upload";

export default function CandidateResumePage() {
  const candidateId = "placeholder";

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Resume</h1>

      <Card>
        <CardHeader>
          <CardTitle>Upload Resume</CardTitle>
        </CardHeader>
        <CardContent>
          <ResumeUpload candidateId={candidateId} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Previous Resumes</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">No resumes uploaded yet.</p>
        </CardContent>
      </Card>
    </div>
  );
}
