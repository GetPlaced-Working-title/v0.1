import { Badge } from "@/components/ui/badge";

interface EvidenceIndicatorProps {
  sources: string[];
}

const sourceLabels: Record<string, string> = {
  resume: "Resume",
  github: "GitHub",
  portfolio: "Portfolio",
  linkedin: "LinkedIn",
  video: "Video",
  certificate: "Certificate",
  recommendation: "Recommendation",
  work_history: "Work History",
};

export function EvidenceIndicator({ sources }: EvidenceIndicatorProps) {
  return (
    <div className="flex flex-wrap gap-1">
      {sources.map((source) => (
        <Badge key={source} variant="secondary" className="text-xs">
          {sourceLabels[source] || source}
        </Badge>
      ))}
    </div>
  );
}
