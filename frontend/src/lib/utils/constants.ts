export const ROLES = {
  CANDIDATE: "candidate",
  RECRUITER: "recruiter",
  ADMIN: "admin",
} as const;

export const EVIDENCE_CONFIDENCE = {
  NONE: "none",
  LOW: "low",
  MEDIUM: "medium",
  HIGH: "high",
  VERY_HIGH: "very_high",
} as const;

export const JOB_STATUS = {
  DRAFT: "draft",
  ACTIVE: "active",
  PAUSED: "paused",
  CLOSED: "closed",
} as const;

export const EMPLOYMENT_TYPES = [
  "full_time",
  "part_time",
  "contract",
  "internship",
] as const;

export const WORK_MODES = ["remote", "hybrid", "onsite"] as const;

export const AVAILABILITY = [
  "immediate",
  "2_weeks",
  "1_month",
  "3_months",
] as const;
