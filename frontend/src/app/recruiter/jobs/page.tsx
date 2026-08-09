"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { JobForm } from "@/components/recruiter/job-form";
import { statusColor } from "@/lib/utils/format";

export default function RecruiterJobsPage() {
  const [showForm, setShowForm] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Jobs</h1>
        <Button onClick={() => setShowForm(!showForm)}>
          {showForm ? "Cancel" : "Create Job"}
        </Button>
      </div>

      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>New Job Posting</CardTitle>
          </CardHeader>
          <CardContent>
            <JobForm
              onSubmit={async (data) => {
                console.log("create job", data);
                setShowForm(false);
              }}
            />
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Your Jobs</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {/* Example job listing */}
            <div className="flex items-center justify-between rounded-lg border p-4">
              <div>
                <h3 className="font-semibold">No jobs posted yet</h3>
                <p className="text-sm text-muted-foreground">Create your first job posting above</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
