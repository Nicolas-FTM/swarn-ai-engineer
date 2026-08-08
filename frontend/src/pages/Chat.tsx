import React, { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import ChatWindow from '../components/chat_window/ChatWindow';

const Chat: React.FC = () => {
  const { state, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!state.isAuthenticated) {
      navigate('/login');
    }
  }, [state.isAuthenticated, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-gray-900">Bakery</h1>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">Hello, {state.user?.full_name} ({state.user?.role})</span>
            <button
              onClick={handleLogout}
              className="bg-amber-600 text-white px-3 py-1 rounded-md text-sm hover:bg-amber-700 transition-colors"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

      <ChatWindow />
    </div>
  );
};

export default Chat;