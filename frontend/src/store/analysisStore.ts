import { create } from 'zustand'
import { Node, Edge } from 'reactflow'

interface AnalysisState {
  currentProject: any | null
  nodes: Node[]
  edges: Edge[]
  analysisResults: any
  progress: {
    agent: string
    progress: number
    message: string
  } | null
  setCurrentProject: (project: any) => void
  setNodes: (nodes: Node[]) => void
  setEdges: (edges: Edge[]) => void
  setAnalysisResults: (results: any) => void
  setProgress: (progress: any) => void
  reset: () => void
}

export const useAnalysisStore = create<AnalysisState>((set) => ({
  currentProject: null,
  nodes: [],
  edges: [],
  analysisResults: null,
  progress: null,
  setCurrentProject: (project) => set({ currentProject: project }),
  setNodes: (nodes) => set({ nodes }),
  setEdges: (edges) => set({ edges }),
  setAnalysisResults: (results) => set({ analysisResults: results }),
  setProgress: (progress) => set({ progress }),
  reset: () => set({
    currentProject: null,
    nodes: [],
    edges: [],
    analysisResults: null,
    progress: null
  })
}))

