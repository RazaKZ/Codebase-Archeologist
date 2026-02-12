import { ArrowLeft, Github, Sparkles } from 'lucide-react'

interface HeaderProps {
  onBack: () => void
}

export default function Header({ onBack }: HeaderProps) {
  return (
    <header className="bg-slate-800/80 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="flex items-center gap-2 px-4 py-2 text-slate-300 hover:text-white hover:bg-slate-700/50 rounded-lg transition-all duration-200"
            >
              <ArrowLeft className="w-5 h-5" />
              <span className="hidden sm:inline">Back to Home</span>
            </button>
            <div className="h-6 w-px bg-slate-600"></div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-slate-700 rounded-lg flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-slate-300" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">
                  Codebase Archeologist
                </h1>
                <p className="text-xs text-slate-400">Analysis Dashboard</p>
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-slate-400 hover:text-white hover:bg-slate-700/50 rounded-lg transition-all duration-200"
              title="GitHub"
            >
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </header>
  )
}

