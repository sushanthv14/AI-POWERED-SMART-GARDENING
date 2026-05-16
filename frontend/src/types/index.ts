export interface PredictionResponse {
  plant_name: string;
  plant_confidence: number;
  disease_name: string;
  disease_confidence: number;
  is_healthy: boolean;
  summary: string;
  recommended_next_step: string;
}

export interface PlantProfile {
  id: string;
  name: string;
  description: string;
  ideal_temperature: string;
  water_frequency: string;
}

export interface RecommendationRequest {
  plant_id: string;
  location: string;
  climate: string;
}

export interface RecommendationResponse {
  recommendations: string[];
  care_tips: string[];
}

export interface ApiError {
  message: string;
  status: number;
}
