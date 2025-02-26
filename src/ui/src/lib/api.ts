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
