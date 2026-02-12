import { useState, useEffect } from 'react'
import { Play, Loader2, XCircle } from 'lucide-react'
import { useAnalysisStore } from '../store/analysisStore'
import { startAnalysis, connectWebSocket, getAnalysisStatus, getAnalysisResults } from '../services/api'

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
      console.log('🚀 Starting analysis for:', repoUrl)
      console.log('🆔 Client ID:', clientId)
      
      const response = await startAnalysis(repoUrl, clientId)
      console.log('📦 Analysis start response:', response)
      
      if (!response.project_id) {
        throw new Error('Failed to get project ID from server')
      }
      
      console.log('✅ Project created with ID:', response.project_id)
      setCurrentProject({ id: response.project_id, repo_url: repoUrl })
      
      // Connect WebSocket for real-time updates
      console.log('🔌 Connecting WebSocket with clientId:', clientId)
      connectWebSocket(clientId, (data) => {
        console.log('📨 WebSocket message received:', data)
        if (data.type === 'progress') {
          console.log(`📊 Progress: ${data.agent} - ${data.progress}% - ${data.message}`)
          setProgress({
            agent: data.agent,
            progress: data.progress,
            message: data.message
          })
        } else if (data.type === 'result') {
          console.log(`✅ Result received from ${data.agent}:`, data.data)
          if (data.agent === 'dependency_mapper') {
            // Transform graph data for React Flow
            const { nodes, edges } = transformGraphData(data.data)
            console.log(`📈 Setting graph: ${nodes.length} nodes, ${edges.length} edges`)
            setNodes(nodes)
            setEdges(edges)
          }
          
          setAnalysisResults((prev: any) => ({
            ...prev,
            [data.agent]: data.data
          }))
        }
      })

      // Wait a bit before starting to poll (give backend time to create project)
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Poll for results
      let statusCheckInterval: NodeJS.Timeout | null = null
      let retryCount = 0
      const maxRetries = 5 // Stop after 5 consecutive 404s
      
      statusCheckInterval = setInterval(async () => {
        try {
          const status = await getAnalysisStatus(response.project_id)
          retryCount = 0 // Reset retry count on success
          console.log('📊 Status check:', status)
          
          if (status.status === 'completed') {
            console.log('✅ Analysis completed!')
            if (statusCheckInterval) clearInterval(statusCheckInterval)
            setLoading(false)
            
            // Fetch final results
            console.log('📥 Fetching final results...')
            const results = await getAnalysisResults(response.project_id)
            console.log('📦 Final results:', results)
            setAnalysisResults(results.results)
            
            // Extract and set graph nodes/edges from dependency_mapper results
            if (results.results?.dependency_mapper) {
              const { nodes, edges } = transformGraphData(results.results.dependency_mapper)
              console.log(`📈 Setting final graph: ${nodes.length} nodes, ${edges.length} edges`)
              setNodes(nodes)
              setEdges(edges)
            } else {
              console.warn('⚠️ No dependency_mapper results found')
            }
          } else if (status.status === 'failed') {
            console.error('❌ Analysis failed')
            if (statusCheckInterval) clearInterval(statusCheckInterval)
            setLoading(false)
            setError('Analysis failed')
          } else {
            console.log(`⏳ Analysis status: ${status.status}`)
          }
        } catch (err: any) {
          // Handle 404 - project might not exist yet or was deleted
          if (err.response?.status === 404) {
            retryCount++
            console.warn(`⚠️ Project not found (404), retry ${retryCount}/${maxRetries}`)
            if (retryCount >= maxRetries) {
              if (statusCheckInterval) clearInterval(statusCheckInterval)
              setLoading(false)
              setError('Project not found. Please try starting a new analysis.')
            }
          } else {
            console.error('❌ Status check error:', err)
          }
        }
      }, 2000)

      // Cleanup after 5 minutes
      setTimeout(() => {
        if (statusCheckInterval) clearInterval(statusCheckInterval)
        if (loading) {
          setLoading(false)
          setError('Analysis timeout. Please try again.')
        }
      }, 300000) // 5 min timeout
      
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

