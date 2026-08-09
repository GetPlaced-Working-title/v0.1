export interface Job {
  id: string;
  company_id: string;
  title: string;
  description: string;
  requirements?: Record<string, unknown>;
  responsibilities?: string[];
  required_skills?: string[];
  preferred_skills?: string[];
  experience_min?: number;
  experience_max?: number;
  education_level?: string;
  employment_type?: string;
  work_mode?: string;
  location?: string;
  salary_min?: number;
  salary_max?: number;
  salary_currency: string;
  benefits?: string[];
  status: string;
  applications_count: number;
  matches_count: number;
  expires_at?: string;
  created_at: string;
  updated_at: string;
}

export interface JobMatch {
  id: string;
  job_id: string;
  candidate_id: string;
  vector_score?: number;
  keyword_score?: number;
  hybrid_score?: number;
  rerank_score?: number;
  final_score?: number;
  rank?: number;
  match_details?: Record<string, unknown>;
  strengths?: Record<string, unknown>;
  gaps?: Record<string, unknown>;
  interview_questions?: Record<string, unknown>;
  status: string;
  recruiter_notes?: string;
  created_at: string;
}
