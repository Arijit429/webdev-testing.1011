import { useState } from 'react'
import Sidebar from './components/Sidebar'
import MobileNav from './components/MobileNav'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import Quizzes from './pages/Quizzes'
import Calendar from './pages/Calendar'
import Analytics from './pages/Analytics'
import Profile from './pages/Profile'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')

  return (
    <div className="app">
      <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      
      <main className="main-content">
        {currentPage === 'dashboard' && <Dashboard setCurrentPage={setCurrentPage} />}
        {currentPage === 'chat' && <Chat />}
        {currentPage === 'quizzes' && <Quizzes />}
        {currentPage === 'calendar' && <Calendar />}
        {currentPage === 'analytics' && <Analytics />}
        {currentPage === 'profile' && <Profile />}
      </main>

      <MobileNav currentPage={currentPage} setCurrentPage={setCurrentPage} />
    </div>
  )
}

export default App
