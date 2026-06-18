import { useState, useEffect } from 'react'
import './App.css'
import ChatWindow from './components/ChatWindow'
import DocumentUpload from './components/DocumentUpload'
import Navbar from './components/Navbar'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)

  useEffect(() => {
    // Check if user is authenticated on mount
    checkAuth()
  }, [])

  const checkAuth = async () => {
    // TODO: Check authentication status
  }

  return (
    <div className="App">
      <Navbar isAuthenticated={isAuthenticated} user={user} />
      <main className="container">
        {isAuthenticated ? (
          <div className="dashboard">
            <div className="sidebar">
              <DocumentUpload />
            </div>
            <div className="main-content">
              <ChatWindow />
            </div>
          </div>
        ) : (
          <div className="login-page">
            <h1>Welcome to Swarn RAG Chatbot</h1>
            <p>Please login to continue</p>
            {/* TODO: Add login form */}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
