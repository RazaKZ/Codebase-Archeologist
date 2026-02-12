import { useCallback, useEffect } from 'react'
import ReactFlow, {
  Controls,
  Background,
  MiniMap,
  useNodesState,
  useEdgesState,
  Connection,
  addEdge,
} from 'reactflow'
import { Network } from 'lucide-react'
import 'reactflow/dist/style.css'
import { useAnalysisStore } from '../store/analysisStore'

export default function GraphVisualization() {
  const { nodes: storeNodes, edges: storeEdges } = useAnalysisStore()
  const [nodes, setNodes, onNodesChange] = useNodesState(storeNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(storeEdges)

  useEffect(() => {
    setNodes(storeNodes)
    setEdges(storeEdges)
  }, [storeNodes, storeEdges, setNodes, setEdges])

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  if (nodes.length === 0 && edges.length === 0) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700/50" style={{ height: '600px' }}>
        <div className="flex items-center justify-center h-full text-slate-400">
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-4 bg-slate-700/50 rounded-full flex items-center justify-center">
              <Network className="w-8 h-8 text-slate-500" />
            </div>
            <p className="text-lg font-semibold mb-2">No graph data available</p>
            <p className="text-sm text-slate-500">Waiting for analysis to complete...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-700/50 overflow-hidden" style={{ height: '600px' }}>
      <div className="absolute top-4 left-4 z-10 px-3 py-1.5 bg-slate-900/80 backdrop-blur-sm rounded-lg border border-slate-700/50">
        <div className="flex items-center gap-2 text-sm">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-slate-300">
            {nodes.length} nodes • {edges.length} connections
          </span>
        </div>
      </div>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
        className="bg-slate-900"
      >
        <Controls className="bg-slate-800/90 border border-slate-700/50 rounded-lg" />
        <MiniMap 
          className="bg-slate-800/90 border border-slate-700/50 rounded-lg"
          nodeColor={() => {
            return '#6366f1'
          }}
        />
        <Background variant="dots" gap={16} size={1} />
      </ReactFlow>
    </div>
  )
}

