export interface Candidate {
  id: string;
  user_id: string;
  name: string;
  headline?: string;
  location?: string;
  phone?: string;
  bio?: string;
  years_of_experience?: number;
  current_role?: string;
  current_company?: string;
  preferred_roles?: string[];
  preferred_locations?: string[];
  open_to_remote: boolean;
  salary_expectation_min?: number;
  salary_expectation_max?: number;
  salary_currency: string;
  availability?: string;
  profile_completeness: number;
  evidence_confidence: string;
  profile_summary?: Record<string, unknown>;
  overall_scores?: Record<string, number>;
  last_analyzed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface Skill {
  id: string;
  candidate_id: string;
  name: string;
  category?: string;
  confidence: string;
  evidence_sources?: Record<string, unknown>;
  proficiency_level?: string;
  verified: boolean;
}

export interface Resume {
  id: string;
  candidate_id: string;
  file_url: string;
  file_name?: string;
  analysis?: Record<string, unknown>;
  scores?: Record<string, number>;
  processing_status: string;
  is_primary: boolean;
  analyzed_at?: string;
  created_at: string;
}

export interface GitHubProfile {
  id: string;
  candidate_id: string;
  username: string;
  profile_url?: string;
  public_repos?: number;
  followers?: number;
  total_stars?: number;
  primary_languages?: Record<string, number>;
  analysis?: Record<string, unknown>;
  scores?: Record<string, number>;
  processing_status: string;
  analyzed_at?: string;
}

export interface Portfolio {
  id: string;
  candidate_id: string;
  url: string;
  title?: string;
  portfolio_type?: string;
  analysis?: Record<string, unknown>;
  scores?: Record<string, number>;
  processing_status: string;
}

export interface Project {
  id: string;
  candidate_id: string;
  title: string;
  description?: string;
  role?: string;
  technologies?: string[];
  url?: string;
  github_url?: string;
  live_url?: string;
  start_date?: string;
  end_date?: string;
  is_ongoing: boolean;
  scope?: string;
  analysis?: Record<string, unknown>;
  scores?: Record<string, number>;
  processing_status: string;
  created_at: string;
}

export interface Certificate {
  id: string;
  candidate_id: string;
  name: string;
  issuer?: string;
  issue_date?: string;
  credential_url?: string;
  difficulty_level?: string;
  skills_covered?: string[];
  analysis?: Record<string, unknown>;
  scores?: Record<string, number>;
  is_verified: boolean;
  processing_status: string;
}

export interface Video {
  id: string;
  candidate_id: string;
  title?: string;
  file_url: string;
  duration_seconds?: number;
  analysis?: Record<string, unknown>;
  scores?: Record<string, number>;
  processing_status: string;
}

export interface WorkHistory {
  id: string;
  candidate_id: string;
  company: string;
  title: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  is_current: boolean;
  employment_type?: string;
  description?: string;
  responsibilities?: string[];
  achievements?: string[];
  technologies?: string[];
  analysis?: Record<string, unknown>;
}
