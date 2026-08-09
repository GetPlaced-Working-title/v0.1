import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Skill } from "@/lib/types/candidate";

interface SkillBadgeProps {
  skill: Skill;
}

const confidenceStyles: Record<string, string> = {
  very_high: "bg-green-100 text-green-800 border-green-200",
  high: "bg-emerald-100 text-emerald-800 border-emerald-200",
  medium: "bg-yellow-100 text-yellow-800 border-yellow-200",
  low: "bg-orange-100 text-orange-800 border-orange-200",
  resume_mention: "bg-gray-100 text-gray-600 border-gray-200",
  none: "bg-gray-50 text-gray-400 border-gray-100",
};

export function SkillBadge({ skill }: SkillBadgeProps) {
  return (
    <Badge
      variant="outline"
      className={cn("text-xs", confidenceStyles[skill.confidence] || confidenceStyles.none)}
    >
      {skill.name}
      {skill.verified && " ✓"}
    </Badge>
  );
}
