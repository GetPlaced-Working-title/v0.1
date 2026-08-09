import { formatScore } from "@/lib/utils/format";
import { cn } from "@/lib/utils";

interface MatchScoreProps {
  score: number;
  size?: "sm" | "md" | "lg";
}

export function MatchScore({ score, size = "md" }: MatchScoreProps) {
  const percent = Math.round(score * 100);
  const color =
    percent >= 80
      ? "text-green-600"
      : percent >= 60
        ? "text-yellow-600"
        : percent >= 40
          ? "text-orange-500"
          : "text-red-500";

  const sizeClasses = {
    sm: "text-lg",
    md: "text-2xl",
    lg: "text-4xl",
  };

  return (
    <div className="flex flex-col items-center">
      <span className={cn("font-bold", color, sizeClasses[size])}>{percent}%</span>
      <span className="text-xs text-muted-foreground">match</span>
    </div>
  );
}
