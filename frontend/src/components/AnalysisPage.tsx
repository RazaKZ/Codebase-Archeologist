import Dashboard from './Dashboard'
import AnalysisPanel from './AnalysisPanel'
import GraphVisualization from './GraphVisualization'
import Header from './Header'
import Footer from './Footer'
import ChatBot from './ChatBot'
import { useAnalysisStore } from '../store/analysisStore'

interface AnalysisPageProps {
  onBack: () => void
}

export default function AnalysisPage({ onBack }: AnalysisPageProps) {
  const { currentProject } = useAnalysisStore()

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 text-white flex flex-col">
      <Header onBack={onBack} />
      
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="mb-6">
          <h2 className="text-3xl font-bold mb-2 text-white">
            Code Analysis Dashboard
          </h2>
          <p className="text-slate-400">
            Analyze your repository structure, dependencies, and code relationships
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <AnalysisPanel />
          </div>
          <div className="lg:col-span-2">
            {currentProject ? (
              <GraphVisualization />
            ) : (
              <Dashboard />
            )}
          </div>
        </div>
      </main>

      <Footer />
      <ChatBot />
    </div>
  )
}

