import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Auth services
export const authService = {
  login: async (username, password) => {
    const response = await api.post('/api/auth/login', { username, password })
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
    }
    return response.data
  },
  
  register: async (userData) => {
    const response = await api.post('/api/auth/register', userData)
    return response.data
  },
  
  logout: () => {
    localStorage.removeItem('token')
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/api/auth/me')
    return response.data
  },
}

// Document services
export const documentService = {
  getAll: async () => {
    const response = await api.get('/api/documents/')
    return response.data
  },
  
  get: async (id) => {
    const response = await api.get(`/api/documents/${id}`)
    return response.data
  },
  
  create: async (document) => {
    const response = await api.post('/api/documents/', document)
    return response.data
  },
  
  update: async (id, document) => {
    const response = await api.put(`/api/documents/${id}`, document)
    return response.data
  },
  
  delete: async (id) => {
    const response = await api.delete(`/api/documents/${id}`)
    return response.data
  },
  
  sign: async (id, signatureData) => {
    const response = await api.post(`/api/documents/${id}/sign`, null, {
      params: { signature_data: signatureData }
    })
    return response.data
  },
}

// Teaching Hour services
export const teachingHourService = {
  getAll: async () => {
    const response = await api.get('/api/teaching-hours/')
    return response.data
  },
  
  get: async (id) => {
    const response = await api.get(`/api/teaching-hours/${id}`)
    return response.data
  },
  
  create: async (hour) => {
    const response = await api.post('/api/teaching-hours/', hour)
    return response.data
  },
  
  update: async (id, hour) => {
    const response = await api.put(`/api/teaching-hours/${id}`, hour)
    return response.data
  },
  
  delete: async (id) => {
    const response = await api.delete(`/api/teaching-hours/${id}`)
    return response.data
  },
  
  approve: async (id) => {
    const response = await api.post(`/api/teaching-hours/${id}/approve`)
    return response.data
  },
}

// Report services
export const reportService = {
  getAll: async () => {
    const response = await api.get('/api/reports/')
    return response.data
  },
  
  get: async (id) => {
    const response = await api.get(`/api/reports/${id}`)
    return response.data
  },
  
  create: async (report) => {
    const response = await api.post('/api/reports/', report)
    return response.data
  },
  
  delete: async (id) => {
    const response = await api.delete(`/api/reports/${id}`)
    return response.data
  },
  
  exportDocuments: async () => {
    const response = await api.get('/api/reports/export/documents', {
      responseType: 'blob'
    })
    return response.data
  },
  
  exportTeachingHours: async () => {
    const response = await api.get('/api/reports/export/teaching-hours', {
      responseType: 'blob'
    })
    return response.data
  },
}

export default api
