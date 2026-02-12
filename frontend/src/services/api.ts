import axios from 'axios'

// Use environment variable or fallback to localhost for development
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Helper to get WebSocket URL
const getWebSocketUrl = (path: string) => {
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const wsUrl = baseUrl.replace('http://', 'ws://').replace('https://', 'wss://')
  return `${wsUrl}${path}`
}

export async function startAnalysis(repoUrl: string, clientId: string) {
  const response = await axios.post(`${API_BASE}/api/analysis/start`, {
    repo_url: repoUrl,
    client_id: clientId
  })
  return response.data
}

export function connectWebSocket(clientId: string, onMessage: (data: any) => void) {
  const ws = new WebSocket(getWebSocketUrl(`/ws/${clientId}`))
  
  ws.onopen = () => {
    console.log('WebSocket connected')
  }
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage(data)
    } catch (err) {
      console.error('Failed to parse WebSocket message:', err)
    }
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
  
  ws.onclose = () => {
    console.log('WebSocket disconnected')
  }
  
  return ws
}

export async function getAnalysisStatus(projectId: number) {
  const response = await axios.get(`${API_BASE}/api/analysis/status/${projectId}`)
  return response.data
}

export async function getAnalysisResults(projectId: number) {
  const response = await axios.get(`${API_BASE}/api/analysis/results/${projectId}`)
  return response.data
}

export async function analyzeImpact(projectId: number, targetNode: string) {
  const response = await axios.post(`${API_BASE}/api/analysis/impact`, {
    project_id: projectId,
    target_node: targetNode
  })
  return response.data
}

export async function sendChatMessage(message: string, projectId?: number, analysisResults?: any) {
  const response = await axios.post(`${API_BASE}/api/chat`, {
    message,
    project_id: projectId,
    analysis_results: analysisResults
  })
  return response.data
}

