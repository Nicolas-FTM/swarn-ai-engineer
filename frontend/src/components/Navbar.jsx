import './Navbar.css'

function Navbar({ isAuthenticated, user }) {
  return (
    <nav className="navbar">
      <div className="navbar-content">
        <h1 className="logo">Swarn RAG Chatbot</h1>
        <div className="navbar-actions">
          {isAuthenticated && user && (
            <span className="user-info">{user.email}</span>
          )}
        </div>
      </div>
    </nav>
  )
}

export default Navbar
