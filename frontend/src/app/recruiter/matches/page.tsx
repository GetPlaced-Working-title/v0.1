"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function RecruiterMatchesPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Matches</h1>
        <Button>Run Matching</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Job Matches</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Select a job to view its AI-matched candidates. The matching pipeline uses vector search
            to find similar candidates, then AI reranks them by fit.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
