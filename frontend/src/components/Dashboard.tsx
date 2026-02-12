import { FileCode, FunctionSquare, AlertTriangle, GitBranch, TrendingUp, Activity } from 'lucide-react'
import { useAnalysisStore } from '../store/analysisStore'

export default function Dashboard() {
  const { analysisResults, progress } = useAnalysisStore()

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 shadow-xl border border-slate-700/50">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">
          Analysis Dashboard
        </h2>
        {progress && (
          <div className="flex items-center gap-2 px-3 py-1 bg-slate-700/50 rounded-full border border-slate-600/50">
            <Activity className="w-4 h-4 text-slate-400 animate-pulse" />
            <span className="text-sm text-slate-400">Analyzing...</span>
          </div>
        )}
      </div>
      
      {progress && (
        <div className="mb-6 p-4 bg-slate-700/50 rounded-lg border border-slate-600/50">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-semibold text-white">{progress.agent}</span>
            <span className="text-sm font-bold text-slate-300">{Math.round(progress.progress * 100)}%</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2.5 overflow-hidden">
            <div
              className="bg-slate-500 h-2.5 rounded-full transition-all duration-500"
              style={{ width: `${progress.progress * 100}%` }}
            />
          </div>
          <p className="text-sm text-slate-400 mt-3">{progress.message}</p>
        </div>
      )}

      {analysisResults && (
        <div className="space-y-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-slate-700/30 p-5 rounded-xl border border-slate-600/50 hover:border-slate-500/50 transition-all duration-300">
              <div className="flex items-center justify-between mb-2">
                <FileCode className="w-5 h-5 text-slate-400" />
                <span className="text-xs text-slate-400">Files</span>
              </div>
              <div className="text-3xl font-bold text-white">
                {analysisResults.repo_analyzer?.total_files || 0}
              </div>
            </div>
            
            <div className="bg-slate-700/30 p-5 rounded-xl border border-slate-600/50 hover:border-slate-500/50 transition-all duration-300">
              <div className="flex items-center justify-between mb-2">
                <FunctionSquare className="w-5 h-5 text-slate-400" />
                <span className="text-xs text-slate-400">Functions</span>
              </div>
              <div className="text-3xl font-bold text-white">
                {analysisResults.repo_analyzer?.total_functions || 0}
              </div>
            </div>

            <div className="bg-slate-700/30 p-5 rounded-xl border border-slate-600/50 hover:border-slate-500/50 transition-all duration-300">
              <div className="flex items-center justify-between mb-2">
                <GitBranch className="w-5 h-5 text-slate-400" />
                <span className="text-xs text-slate-400">Classes</span>
              </div>
              <div className="text-3xl font-bold text-white">
                {analysisResults.repo_analyzer?.total_classes || 0}
              </div>
            </div>

            <div className="bg-slate-700/30 p-5 rounded-xl border border-slate-600/50 hover:border-slate-500/50 transition-all duration-300">
              <div className="flex items-center justify-between mb-2">
                <TrendingUp className="w-5 h-5 text-slate-400" />
                <span className="text-xs text-slate-400">Nodes</span>
              </div>
              <div className="text-3xl font-bold text-white">
                {analysisResults.dependency_mapper?.nodes?.length || 0}
              </div>
            </div>
          </div>

          {/* Graph Analysis */}
          {analysisResults.dependency_mapper?.analysis && (
            <div className="bg-slate-700/30 backdrop-blur-sm rounded-xl p-6 border border-slate-600/50">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-yellow-400" />
                Code Quality Metrics
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-slate-800/50 rounded-lg border border-red-500/20">
                  <div className="text-sm text-slate-400 mb-1">Dead Functions</div>
                  <div className="text-2xl font-bold text-red-400">
                    {analysisResults.dependency_mapper.analysis.dead_functions?.length || 0}
                  </div>
                </div>
                <div className="p-4 bg-slate-800/50 rounded-lg border border-yellow-500/20">
                  <div className="text-sm text-slate-400 mb-1">Circular Dependencies</div>
                  <div className="text-2xl font-bold text-yellow-400">
                    {analysisResults.dependency_mapper.analysis.circular_dependencies?.length || 0}
                  </div>
                </div>
                <div className="p-4 bg-slate-800/50 rounded-lg border border-orange-500/20">
                  <div className="text-sm text-slate-400 mb-1">High Coupling</div>
                  <div className="text-2xl font-bold text-orange-400">
                    {analysisResults.dependency_mapper.analysis.high_coupling?.length || 0}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {!analysisResults && !progress && (
        <div className="text-center py-16">
          <div className="w-20 h-20 mx-auto mb-4 bg-slate-700/50 rounded-full flex items-center justify-center">
            <FileCode className="w-10 h-10 text-slate-500" />
          </div>
          <p className="text-slate-400 text-lg mb-2">No analysis data yet</p>
          <p className="text-slate-500 text-sm">Start an analysis to see results here</p>
        </div>
      )}
    </div>
  )
}

