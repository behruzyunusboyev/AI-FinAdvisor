import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export function getHealth() {
  return apiClient.get("/health");
}

export function calculateLoan(payload) {
  return apiClient.post("/loan/calculate", payload);
}

export function estimateTax(payload) {
  return apiClient.post("/tax/estimate", payload);
}

export function generateBusinessPlan(payload) {
  return apiClient.post("/business-plan/generate", payload);
}

export function exportBusinessPlanPdf(payload) {
  return apiClient.post("/pdf/export", payload, {
    responseType: "blob",
  });
}

export default apiClient;
