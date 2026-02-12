import { useState } from 'react'
import HomePage from './components/HomePage'
import AnalysisPage from './components/AnalysisPage'

function App() {
  const [currentPage, setCurrentPage] = useState<'home' | 'analysis'>('home')

  return (
    <>
      {currentPage === 'home' ? (
        <HomePage onStartAnalysis={() => setCurrentPage('analysis')} />
      ) : (
        <AnalysisPage onBack={() => setCurrentPage('home')} />
      )}
    </>
  )
}

export default App

