import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { confidenceColor } from "@/lib/utils/format";
import type { Candidate } from "@/lib/types/candidate";

interface ProfileCardProps {
  candidate: Candidate;
}

export function ProfileCard({ candidate }: ProfileCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle>{candidate.name}</CardTitle>
            {candidate.headline && (
              <p className="text-sm text-muted-foreground mt-1">{candidate.headline}</p>
            )}
          </div>
          <Badge className={confidenceColor(candidate.evidence_confidence)}>
            {candidate.evidence_confidence.replace("_", " ")}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4 text-sm">
          {candidate.location && (
            <div>
              <span className="text-muted-foreground">Location:</span>{" "}
              {candidate.location}
            </div>
          )}
          {candidate.current_role && (
            <div>
              <span className="text-muted-foreground">Role:</span>{" "}
              {candidate.current_role}
              {candidate.current_company && ` at ${candidate.current_company}`}
            </div>
          )}
          {candidate.years_of_experience && (
            <div>
              <span className="text-muted-foreground">Experience:</span>{" "}
              {candidate.years_of_experience} years
            </div>
          )}
          {candidate.availability && (
            <div>
              <span className="text-muted-foreground">Available:</span>{" "}
              {candidate.availability.replace("_", " ")}
            </div>
          )}
        </div>

        {candidate.open_to_remote && (
          <Badge variant="outline" className="mt-3">Open to Remote</Badge>
        )}
      </CardContent>
    </Card>
  );
}
