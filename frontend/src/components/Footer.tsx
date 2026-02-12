import { Github, Sparkles, Code } from 'lucide-react'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-slate-900 border-t border-slate-800 mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Brand Section */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-slate-700 rounded-lg flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-slate-300" />
              </div>
              <span className="text-lg font-bold text-white">
                Codebase Archeologist
              </span>
            </div>
            <p className="text-slate-400 text-sm leading-relaxed">
              Multi-agent codebase analysis and visualization system powered by AI.
              Understand your codebase architecture, dependencies, and business logic.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Features</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">
                  AST Analysis
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">
                  Dependency Mapping
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">
                  Impact Analysis
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors">
                  Business Logic Extraction
                </a>
              </li>
            </ul>
          </div>

          {/* Contact/Info */}
          <div>
            <h3 className="text-white font-semibold mb-4">About</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-slate-400 hover:text-white text-sm transition-colors flex items-center gap-2">
                  <Code className="w-4 h-4" />
                  Documentation
                </a>
              </li>
              <li>
                <a
                  href="https://github.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-slate-400 hover:text-white text-sm transition-colors flex items-center gap-2"
                >
                  <Github className="w-4 h-4" />
                  GitHub
                </a>
              </li>
              <li>
                <span className="text-slate-400 text-sm">Version 1.0.0</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-6 border-t border-slate-800">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-slate-500 text-sm">
              © {currentYear} Codebase Archeologist. All rights reserved.
            </p>
            <div className="flex items-center gap-6">
              <a href="#" className="text-slate-500 hover:text-slate-400 text-sm transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-slate-500 hover:text-slate-400 text-sm transition-colors">
                Terms of Service
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

