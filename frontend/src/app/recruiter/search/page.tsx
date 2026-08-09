"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SearchFilters } from "@/components/recruiter/search-filters";

export default function RecruiterSearchPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Search Candidates</h1>

      <SearchFilters type="candidates" onSearch={() => console.log("search")} />

      <Card>
        <CardHeader>
          <CardTitle>Results</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Enter search criteria above to find candidates. Results are powered by Meilisearch keyword search
            and Qdrant vector similarity.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
