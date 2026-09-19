import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

export const submitBusinessPlan = (payload) => apiClient.post('/business-plan/generate', payload)
export const dailyCheck = (payload) => apiClient.post('/copilot/daily-check', payload)
export const pdfUrl = (projectId) => `${apiClient.defaults.baseURL}/export/pdf/${projectId}`

export default apiClient
