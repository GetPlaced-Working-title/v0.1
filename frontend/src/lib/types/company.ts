export interface Company {
  id: string;
  user_id: string;
  name: string;
  domain?: string;
  website?: string;
  industry?: string;
  size?: string;
  description?: string;
  logo_url?: string;
  location?: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}
