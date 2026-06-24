import { useEffect, useState } from "react";

import ChatWindow from "./components/chat_window/ChatWindow";
import DocumentUpload from "./components/document_upload/DocumentUpload";
import Navbar from "./components/navbar/Navbar";

type User = {
  id?: string;
  name?: string;
  email?: string;
} | null;

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<User>(null);

  useEffect(() => {
    // Check if user is authenticated on mount
    checkAuth();
  }, []);

  const checkAuth = async (): Promise<void> => {
    // TODO: Check authentication status
  };

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
  );
}

export default App;