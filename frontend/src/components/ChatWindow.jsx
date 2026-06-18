import { useState } from 'react'
import './ChatWindow.css'
import { apiClient } from '../services/api'

function ChatWindow() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSendMessage = async (e) => {
    e.preventDefault()
    
    if (!input.trim()) return

    // Add user message to UI
    const userMessage = { role: 'user', content: input }
    setMessages([...messages, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Send to backend
      const response = await apiClient.post('/api/chat/message', {
        message: input,
      })

      // Add assistant response
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.message,
        sources: response.data.sources || []
      }])
    } catch (error) {
      console.error('Error sending message:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Error: Could not get response from server',
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="content">{msg.content}</div>
            {msg.sources && msg.sources.length > 0 && (
              <div className="sources">
                Sources: {msg.sources.join(', ')}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="message assistant">Thinking...</div>}
      </div>
      
      <form onSubmit={handleSendMessage} className="input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          Send
        </button>
      </form>
    </div>
  )
}

export default ChatWindow
