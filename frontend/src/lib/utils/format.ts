export function formatScore(score: number): string {
  return `${Math.round(score * 100)}%`;
}

export function formatSalary(min?: number, max?: number, currency = "USD"): string {
  const formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  });
  if (min && max) return `${formatter.format(min)} - ${formatter.format(max)}`;
  if (min) return `From ${formatter.format(min)}`;
  if (max) return `Up to ${formatter.format(max)}`;
  return "Not specified";
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
  });
}

export function confidenceColor(confidence: string): string {
  switch (confidence) {
    case "very_high":
      return "text-green-600 bg-green-50";
    case "high":
      return "text-green-500 bg-green-50";
    case "medium":
      return "text-yellow-600 bg-yellow-50";
    case "low":
      return "text-orange-500 bg-orange-50";
    default:
      return "text-gray-400 bg-gray-50";
  }
}

export function statusColor(status: string): string {
  switch (status) {
    case "active":
    case "completed":
      return "text-green-600 bg-green-50";
    case "processing":
    case "pending":
      return "text-blue-600 bg-blue-50";
    case "failed":
    case "closed":
      return "text-red-600 bg-red-50";
    default:
      return "text-gray-500 bg-gray-50";
  }
}
