import { useState, useEffect } from "react";
import { Message } from './useChat';

const API_BASE = "http://localhost:8000"

export type Chat = {
    id: string
    title: string
    messages: Message[]
}

function authHeaders(): HeadersInit {
    const token = localStorage.getItem("access_token")
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    }
}

async function fetchMessages(chatId: string): Promise<Message[]> {
    try {
        const res = await fetch(`${API_BASE}/conversations/${chatId}/messages`, { headers: authHeaders() })
        if (!res.ok) return []
        const data = await res.json()
        return data.map((m: { content: string; system_generated: boolean }) => ({
            role: m.system_generated ? "assistant" : "user",
            text: m.content,
        }))
    } catch { return [] }
}

export function useChats() {
    const [chats, setChats] = useState<Chat[]>([])
    const [activeChatId, setActiveChatId] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(false)

    useEffect(() => {
        async function loadChats() {
            try {
                const res = await fetch(`${API_BASE}/conversations`, { headers: authHeaders() })
                if (!res.ok) return
                const data = await res.json()
                const loaded: Chat[] = data.map((c: { id: string; title: string }) => ({ id: c.id, title: c.title, messages: [] }))
                setChats(loaded)
                const lastActive = localStorage.getItem("active_chat_id")
                if (lastActive && loaded.find(c => c.id === lastActive)) {
                    const messages = await fetchMessages(lastActive)
                    setChats(prev => prev.map(c => c.id === lastActive ? { ...c, messages } : c))
                    setActiveChatId(lastActive)
                }
            } catch { }
        }
        loadChats()
    }, [])

    async function createChat(): Promise<string> {
        try {
            const res = await fetch(`${API_BASE}/conversations`, {
                method: "POST",
                headers: authHeaders(),
                body: JSON.stringify({ title: "New conversation" })
            })
            if (!res.ok) return ""
            const data = await res.json()
            const newChat: Chat = { id: data.id, title: data.title, messages: [] }
            setChats(prev => [newChat, ...prev])
            setActiveChatId(data.id)
            return data.id
        } catch { return "" }
    }

    function addMessage(chatId: string, message: Message) {
        setChats(prev => prev.map(
            chat => chat.id === chatId
                ? { ...chat, messages: [...chat.messages, message] }
                : chat
        ))
    }

    async function deleteChat(chatId: string) {
        try {
            await fetch(`${API_BASE}/conversations/${chatId}`, {
                method: "DELETE",
                headers: authHeaders()
            })
        } catch { }
        setChats(prev => prev.filter(c => c.id !== chatId))
        if (activeChatId === chatId) {
            setActiveChatId(null)
            localStorage.removeItem("active_chat_id")
        }
    }

    async function sendMessageToActiveChat(text: string, imageUrl?: string): Promise<void> {
        if (!activeChatId) return
        setIsLoading(true)

        const userMsg: Message = { role: "user", text, timestamp: new Date().toISOString() }
        addMessage(activeChatId, userMsg)

        await fetch(`${API_BASE}/conversations/${activeChatId}/messages`, {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({ content: text, attachment_url: imageUrl ?? null, system_generated: false })
        })

        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({
                message: text,
                producer_id: "00000000-0000-0000-0000-000000000001",
                image_url: imageUrl ?? null,
                crop_type: "general",
                province_state: "Andhra Pradesh",
                producer_type: 1,
                language: "EN",
            }),
        })
        const data = await res.json()
        const assistantMsg: Message = { role: "assistant", text: data.specialist_response, timestamp: new Date().toISOString() }
        addMessage(activeChatId, assistantMsg)

        await fetch(`${API_BASE}/conversations/${activeChatId}/messages`, {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({ content: data.specialist_response, system_generated: true })
        })

        setIsLoading(false)
    }

    async function selectChat(chatId: string) {
        localStorage.setItem("active_chat_id", chatId)
        setActiveChatId(chatId)
        const alreadyLoaded = chats.find(c => c.id === chatId)?.messages.length ?? 0
        if (alreadyLoaded === 0) {
            const messages = await fetchMessages(chatId)
            setChats(prev => prev.map(c => c.id === chatId ? { ...c, messages } : c))
        }
    }

    return { chats, activeChatId, createChat, setActiveChatId: selectChat, sendMessageToActiveChat, isLoading, deleteChat }
}
