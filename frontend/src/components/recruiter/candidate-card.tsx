import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { confidenceColor, formatScore } from "@/lib/utils/format";
import type { Candidate } from "@/lib/types/candidate";

interface CandidateCardProps {
  candidate: Candidate;
  matchScore?: number;
}

export function CandidateCard({ candidate, matchScore }: CandidateCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <h3 className="font-semibold">{candidate.name}</h3>
            {candidate.headline && (
              <p className="text-sm text-muted-foreground">{candidate.headline}</p>
            )}
          </div>
          {matchScore !== undefined && (
            <div className="text-right">
              <div className="text-2xl font-bold text-primary">{formatScore(matchScore)}</div>
              <p className="text-xs text-muted-foreground">match</p>
            </div>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex flex-wrap gap-2">
            <Badge className={confidenceColor(candidate.evidence_confidence)}>
              {candidate.evidence_confidence.replace("_", " ")} evidence
            </Badge>
            {candidate.years_of_experience && (
              <Badge variant="outline">{candidate.years_of_experience}y exp</Badge>
            )}
            {candidate.open_to_remote && (
              <Badge variant="outline">Remote OK</Badge>
            )}
          </div>

          {candidate.location && (
            <p className="text-sm text-muted-foreground">{candidate.location}</p>
          )}

          <Link href={`/recruiter/candidates/${candidate.id}`}>
            <Button variant="outline" size="sm" className="w-full">View Profile</Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
