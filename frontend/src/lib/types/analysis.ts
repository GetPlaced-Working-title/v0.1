export interface AnalysisScores {
  technical_depth?: number;
  code_quality?: number;
  communication?: number;
  confidence?: number;
  experience_quality?: number;
  project_quality?: number;
  design_quality?: number;
  [key: string]: number | undefined;
}

export interface SkillGapAnalysis {
  missing_skills: string[];
  weak_skills: string[];
  strong_skills: string[];
  recommendations: string[];
}

export interface MatchResult {
  candidate_id: string;
  candidate_name: string;
  final_score: number;
  vector_score?: number;
  keyword_score?: number;
  rerank_score?: number;
  match_details?: Record<string, unknown>;
  strengths?: string[];
  gaps?: string[];
}
