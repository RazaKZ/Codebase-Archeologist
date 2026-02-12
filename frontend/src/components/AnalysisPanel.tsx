import { useState, useEffect } from 'react'
import { Play, Loader2, CheckCircle2, XCircle } from 'lucide-react'
import { useAnalysisStore } from '../store/analysisStore'
import { startAnalysis, connectWebSocket } from '../services/api'

// Helper function to transform graph data for React Flow
function transformGraphData(graphData: any) {
  if (!graphData || !graphData.nodes || !graphData.edges) {
    return { nodes: [], edges: [] }
  }
  
  const nodes = graphData.nodes.map((node: any, index: number) => ({
    id: node.id,
    type: 'default',
    position: { 
      x: (index % 10) * 150, 
      y: Math.floor(index / 10) * 100 
    },
    data: { label: node.name || node.id || node.file || node.id }
  }))
  
  const edges = graphData.edges.map((edge: any) => ({
    id: `${edge.source}-${edge.target}`,
    source: edge.source,
    target: edge.target,
    type: 'smoothstep'
  }))
  
  return { nodes, edges }
}

export default function AnalysisPanel() {
  const { currentProject, setCurrentProject, setProgress, setNodes, setEdges, setAnalysisResults } = useAnalysisStore()
  const [repoUrl, setRepoUrl] = useState(currentProject?.repo_url || '')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Update repoUrl when currentProject changes
  useEffect(() => {
    if (currentProject?.repo_url) {
      setRepoUrl(currentProject.repo_url)
    }
  }, [currentProject])

  const handleAnalyze = async () => {
    if (!repoUrl.trim()) {
      setError('Please enter a repository URL')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const clientId = `client_${Date.now()}`
      const response = await startAnalysis(repoUrl, clientId)
      
      setCurrentProject({ id: response.project_id, repo_url: repoUrl })
      
      // Connect WebSocket for real-time updates
      connectWebSocket(clientId, (data) => {
        if (data.type === 'progress') {
          setProgress({
            agent: data.agent,
            progress: data.progress,
            message: data.message
          })
        } else if (data.type === 'result') {
          if (data.agent === 'dependency_mapper') {
            // Transform graph data for React Flow
            const { nodes, edges } = transformGraphData(data.data)
            setNodes(nodes)
            setEdges(edges)
          }
          
          setAnalysisResults((prev: any) => ({
            ...prev,
            [data.agent]: data.data
          }))
        }
      })

      // Poll for results
      const checkStatus = setInterval(async () => {
        try {
          const statusResponse = await fetch(`http://localhost:8000/api/analysis/status/${response.project_id}`)
          const status = await statusResponse.json()
          
          if (status.status === 'completed') {
            clearInterval(checkStatus)
            setLoading(false)
            
            // Fetch final results
            const resultsResponse = await fetch(`http://localhost:8000/api/analysis/results/${response.project_id}`)
            const results = await resultsResponse.json()
            setAnalysisResults(results.results)
            
            // Extract and set graph nodes/edges from dependency_mapper results
            if (results.results?.dependency_mapper) {
              const { nodes, edges } = transformGraphData(results.results.dependency_mapper)
              setNodes(nodes)
              setEdges(edges)
            }
          } else if (status.status === 'failed') {
            clearInterval(checkStatus)
            setLoading(false)
            setError('Analysis failed')
          }
        } catch (err) {
          console.error('Status check error:', err)
        }
      }, 2000)

      setTimeout(() => clearInterval(checkStatus), 300000) // 5 min timeout
      
    } catch (err: any) {
      setError(err.message || 'Failed to start analysis')
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 shadow-xl border border-slate-700/50">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2 text-white">
          Start Analysis
        </h2>
        <p className="text-sm text-slate-400">
          Enter a GitHub repository URL to begin analysis
        </p>
      </div>
      
      <div className="space-y-5">
        <div>
          <label className="block text-sm font-semibold mb-2 text-slate-300">
            Repository URL
          </label>
          <div className="relative">
            <input
              type="text"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/username/repository"
              className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 text-white placeholder-slate-500 transition-all duration-200"
              disabled={loading}
            />
          </div>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={loading || !repoUrl.trim()}
          className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-slate-700 hover:bg-slate-600 disabled:bg-slate-600 disabled:cursor-not-allowed rounded-lg font-semibold transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] border border-slate-600 hover:border-slate-500 disabled:border-slate-700"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Play size={20} />
              <span>Analyze Repository</span>
            </>
          )}
        </button>

        {error && (
          <div className="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
            <XCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <div className="pt-4 border-t border-slate-700/50">
          <p className="text-xs text-slate-500 text-center">
            Analysis may take a few minutes depending on repository size
          </p>
        </div>
      </div>
    </div>
  )
}

