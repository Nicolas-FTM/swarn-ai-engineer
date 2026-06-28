import { useState, useEffect } from 'react'

const SESSION_STORAGE_KEY = 'chat_session_id'

/**
 * Manages a persistent LangGraph thread/session id for the chat.
 * Generated once per browser session and persisted in localStorage,
 * so a page refresh does not break conversation continuity.
 */
export function useChatSession(): string {
  const [sessionId] = useState<string>(() => {
    const existing = localStorage.getItem(SESSION_STORAGE_KEY)
    if (existing) return existing

    const generated = crypto.randomUUID()
    localStorage.setItem(SESSION_STORAGE_KEY, generated)
    return generated
  })

  return sessionId
}

/**
 * Clears the persisted chat session id. Must be called on logout to
 * prevent the next user on the same browser from inheriting a thread
 * that may contain another role's conversation context.
 */
export function clearChatSession(): void {
  localStorage.removeItem(SESSION_STORAGE_KEY)
}