import apiClient from '../api/apiClient';
import {
  PredictionResponse,
  PlantProfile,
  RecommendationRequest,
  RecommendationResponse,
} from '../types';

/**
 * Predict plant disease from image
 */
export const predictDisease = async (
  imageFile: File
): Promise<PredictionResponse> => {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await apiClient.post<PredictionResponse>(
    '/predict/',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );

  return response.data;
};

/**
 * Get all plant profiles
 */
export const getPlantProfiles = async (): Promise<PlantProfile[]> => {
  const response = await apiClient.get<PlantProfile[]>('/plants/');
  return response.data;
};

/**
 * Get single plant profile by ID
 */
export const getPlantProfile = async (
  plantId: string
): Promise<PlantProfile> => {
  const response = await apiClient.get<PlantProfile>(`/plants/${plantId}`);
  return response.data;
};

/**
 * Get care recommendations for a plant
 */
export const getRecommendations = async (
  request: RecommendationRequest
): Promise<RecommendationResponse> => {
  const response = await apiClient.post<RecommendationResponse>(
    '/recommend/care',
    request
  );
  return response.data;
};
