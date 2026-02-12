import { useState } from 'react'
import { Play, Code, Network, Brain, Zap, ArrowRight, Github, Sparkles } from 'lucide-react'
import { useAnalysisStore } from '../store/analysisStore'

interface HomePageProps {
  onStartAnalysis: () => void
}

export default function HomePage({ onStartAnalysis }: HomePageProps) {
  const [repoUrl, setRepoUrl] = useState('')
  const { setCurrentProject, reset } = useAnalysisStore()

  const handleQuickStart = () => {
    // Reset previous analysis
    reset()
    
    if (repoUrl.trim()) {
      setCurrentProject({ id: 0, repo_url: repoUrl })
    }
    onStartAnalysis()
  }

  const features = [
    {
      icon: <Code className="w-8 h-8" />,
      title: "AST Analysis",
      description: "Deep code structure analysis using advanced parsing techniques"
    },
    {
      icon: <Network className="w-8 h-8" />,
      title: "Dependency Mapping",
      description: "Visualize complex relationships and dependencies in your codebase"
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI-Powered Insights",
      description: "Get intelligent business logic extraction and code understanding"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Impact Analysis",
      description: "Understand what breaks when you modify or delete code components"
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Subtle animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-slate-700/30 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-slate-600/30 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-slate-700/20 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10">
        {/* Navigation */}
        <nav className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-10 h-10 bg-slate-700 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-slate-300" />
                </div>
                <span className="text-2xl font-bold text-white">
                  Codebase Archeologist
                </span>
              </div>
            <button
              onClick={() => {
                reset()
                onStartAnalysis()
              }}
              className="px-6 py-2 bg-slate-800/50 hover:bg-slate-700/50 backdrop-blur-sm rounded-lg border border-slate-700/50 transition-all duration-300"
            >
              Get Started
            </button>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="container mx-auto px-4 py-20">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-slate-800/50 backdrop-blur-sm rounded-full border border-slate-700/50 mb-8">
              <Sparkles className="w-4 h-4 text-slate-400" />
              <span className="text-sm text-slate-300">AI-Powered Code Analysis</span>
            </div>
            
            <h1 className="text-6xl md:text-7xl font-bold mb-6">
              <span className="text-white">
                Decode Your
              </span>
              <br />
              <span className="bg-gradient-to-r from-slate-200 to-slate-400 bg-clip-text text-transparent">
                Codebase
              </span>
            </h1>
            
            <p className="text-xl text-slate-300 mb-12 max-w-2xl mx-auto leading-relaxed">
              Multi-agent system that analyzes your codebase, maps dependencies, extracts business logic, 
              and visualizes the architecture of your software projects.
            </p>

            {/* Quick Start Input */}
            <div className="max-w-2xl mx-auto mb-12">
              <div className="flex flex-col sm:flex-row gap-4 p-2 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700/50">
                <div className="flex-1 flex items-center gap-3 px-4">
                  <Github className="w-5 h-5 text-slate-400" />
                  <input
                    type="text"
                    value={repoUrl}
                    onChange={(e) => setRepoUrl(e.target.value)}
                    placeholder="https://github.com/username/repository"
                    className="flex-1 bg-transparent border-none outline-none text-white placeholder-slate-500"
                  />
                </div>
                <button
                  onClick={handleQuickStart}
                  className="px-8 py-4 bg-slate-700 hover:bg-slate-600 rounded-xl font-semibold flex items-center justify-center gap-2 transition-all duration-300 transform hover:scale-105 border border-slate-600 hover:border-slate-500"
                >
                  <Play className="w-5 h-5" />
                  Analyze Now
                </button>
              </div>
              <p className="text-sm text-slate-400 mt-4">
                Or <button onClick={() => { reset(); onStartAnalysis(); }} className="text-purple-400 hover:text-purple-300 underline">start with an empty analysis</button>
              </p>
            </div>
          </div>

          {/* Features Grid */}
          <div className="max-w-6xl mx-auto mt-32">
            <h2 className="text-3xl font-bold text-center mb-12 text-white">
              Powerful Features
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="group p-6 bg-slate-800/50 backdrop-blur-sm rounded-2xl border border-slate-700/50 hover:border-slate-600 transition-all duration-300 hover:transform hover:scale-105"
                >
                  <div className="w-14 h-14 bg-slate-700/50 rounded-xl flex items-center justify-center mb-4 text-slate-300 group-hover:bg-slate-700 transition-all duration-300">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-white">{feature.title}</h3>
                  <p className="text-slate-400 text-sm leading-relaxed">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Stats Section */}
          <div className="max-w-4xl mx-auto mt-32 mb-20">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-5xl font-bold text-white mb-2">
                  4+
                </div>
                <div className="text-slate-400">AI Agents</div>
              </div>
              <div className="text-center">
                <div className="text-5xl font-bold text-white mb-2">
                  ∞
                </div>
                <div className="text-slate-400">Repositories</div>
              </div>
              <div className="text-center">
                <div className="text-5xl font-bold text-white mb-2">
                  ⚡
                </div>
                <div className="text-slate-400">Real-time Analysis</div>
              </div>
            </div>
          </div>

          {/* CTA Section */}
          <div className="max-w-4xl mx-auto text-center">
            <div className="p-12 bg-slate-800/50 backdrop-blur-sm rounded-3xl border border-slate-700/50">
              <h2 className="text-4xl font-bold mb-4 text-white">Ready to Explore Your Codebase?</h2>
              <p className="text-slate-300 mb-8 text-lg">
                Start analyzing your repository now and discover hidden patterns in your code.
              </p>
              <button
                onClick={() => {
                  reset()
                  onStartAnalysis()
                }}
                className="px-8 py-4 bg-slate-700 hover:bg-slate-600 rounded-xl font-semibold flex items-center justify-center gap-2 mx-auto transition-all duration-300 transform hover:scale-105 border border-slate-600 hover:border-slate-500"
              >
                Get Started
                <ArrowRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

