import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api/v1";

export const uploadReceipt = async (file: File) => {
  const formData = new FormData();
  formData.append("image", file);
  return axios.post(`${API_BASE_URL}/receipt`, formData);
};

export const fetchReceipts = async () => axios.get(`${API_BASE_URL}/receipts`);
export const fetchAnalytics = async () => axios.get(`${API_BASE_URL}/receipts/analytics`);
export const updateReceipt = async (id: number, data: any) => {
  return await axios.post(`${API_BASE_URL}/receipts/${id}`, data);
};
export const deleteReceipt = async (id: number) => axios.delete(`${API_BASE_URL}/receipts/${id}`);
export const searchReceipts = async (query: string) => axios.get(`${API_BASE_URL}/receipts/search?${query}`);

// Authentication APIs
export const getGoogleLoginUrl = async () => {
  const response = await axios.get(`${API_BASE_URL}/auth/google`);
  return response.data.auth_url;
};

export const getUserSession = async () => axios.get(`${API_BASE_URL}/auth/user`, { withCredentials: true });

export const logoutUser = async () => axios.post(`${API_BASE_URL}/auth/logout`, {}, { withCredentials: true });

export async function handleGoogleCallback(code: string): Promise<void> {
  const response: any = await axios.post(`${API_BASE_URL}/auth/callback`, { code });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to authenticate with Google');
  }

  // The backend will set any necessary cookies/tokens
  await response.json();
}
