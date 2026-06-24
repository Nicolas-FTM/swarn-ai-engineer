import { useState } from 'react'
import styles from "./ChatWindow.module.css";
import { apiClient } from '../../services/api'

type Role = 'user' | 'assistant'

interface ChatMessage {
  role: Role
  content: string
  sources?: string[]
}

function ChatWindow() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)

  const handleSendMessage = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    if (!input.trim()) return

    const userMessage: ChatMessage = { role: 'user', content: input }

    setMessages([...messages, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await apiClient.post('/api/chat/message', {
        message: input,
      })

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: response.data.message,
          sources: response.data.sources || [],
        },
      ])
    } catch (error) {
      console.error('Error sending message:', error)

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: 'Error: Could not get response from server',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles["chat-window"]}>
      <div className={styles["messages"]}>
        {messages.map((msg, idx) => (
          <div key={idx} className={styles[`message ${msg.role}`]}>
            <div className={styles["content"]}>{msg.content}</div>

            {msg.sources && msg.sources.length > 0 && (
              <div className={styles["sources"]}>
                Sources: {msg.sources.join(', ')}
              </div>
            )}
          </div>
        ))}

        {loading && <div className={styles["message assistant"]}>Thinking...</div>}
      </div>

      <form onSubmit={handleSendMessage} className={styles["input-form"]}>
        <input
          type="text"
          value={input}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setInput(e.target.value)
          }
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