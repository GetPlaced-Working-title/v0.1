"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { SearchFilters } from "@/components/recruiter/search-filters";
import { CandidateCard } from "@/components/recruiter/candidate-card";

export default function RecruiterCandidatesPage() {
  const [results, setResults] = useState([]);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Candidates</h1>

      <SearchFilters type="candidates" onSearch={() => console.log("search")} />

      <Card>
        <CardHeader>
          <CardTitle>Search Results</CardTitle>
        </CardHeader>
        <CardContent>
          {results.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              No candidates found. Try adjusting your search filters.
            </p>
          ) : (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              {/* Map results here */}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
