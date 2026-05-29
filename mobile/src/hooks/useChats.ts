import { useState, useEffect } from "react"
import AsyncStorage from "@react-native-async-storage/async-storage"
import { Message } from "./useChat"
import { decodeToken } from "../utils/token"
import { API_BASE } from "../constants/api"

export type Chat = {
    id: string
    title: string
    messages: Message[]
}

export function useChats({
    token,
    language = "EN",
    provinceState = "general",
    country = "CA",
}: {
    token: string | null
    language?: string
    provinceState?: string
    country?: string
}) {
    const [chats, setChats] = useState<Chat[]>([])
    const [activeChatId, setActiveChatId] = useState<string | null>(null)
    const [isLoading, setIsLoading] = useState(false)

    function authHeaders(): HeadersInit {
        return {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        }
    }

    function getProducerId(): string {
        if (!token) return ""
        return decodeToken(token)?.user_id ?? ""
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

    useEffect(() => {
        if (!token) return
        async function loadChats() {
            try {
                const res = await fetch(`${API_BASE}/conversations`, { headers: authHeaders() })
                if (!res.ok) return
                const data = await res.json()
                const loaded: Chat[] = data.map((c: { id: string; title: string }) => ({
                    id: c.id,
                    title: c.title,
                    messages: [],
                }))
                setChats(loaded)
                const lastActive = await AsyncStorage.getItem("active_chat_id")
                if (lastActive && loaded.find(c => c.id === lastActive)) {
                    const messages = await fetchMessages(lastActive)
                    setChats(prev => prev.map(c => c.id === lastActive ? { ...c, messages } : c))
                    setActiveChatId(lastActive)
                }
            } catch { }
        }
        loadChats()
    }, [token])

    async function createChat(): Promise<string> {
        try {
            const res = await fetch(`${API_BASE}/conversations`, {
                method: "POST",
                headers: authHeaders(),
                body: JSON.stringify({ title: "New conversation" }),
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
        setChats(prev => prev.map(chat =>
            chat.id === chatId ? { ...chat, messages: [...chat.messages, message] } : chat
        ))
    }

    function updateLastAssistantMessage(chatId: string, text: string) {
        setChats(prev => prev.map(chat => {
            if (chat.id !== chatId) return chat
            const messages = [...chat.messages]
            const lastIdx = messages.length - 1
            if (lastIdx >= 0 && messages[lastIdx].role === "assistant") {
                messages[lastIdx] = { ...messages[lastIdx], text }
            }
            return { ...chat, messages }
        }))
    }

    async function deleteChat(chatId: string) {
        try {
            await fetch(`${API_BASE}/conversations/${chatId}`, {
                method: "DELETE",
                headers: authHeaders(),
            })
        } catch { }
        setChats(prev => prev.filter(c => c.id !== chatId))
        if (activeChatId === chatId) {
            setActiveChatId(null)
            await AsyncStorage.removeItem("active_chat_id")
        }
    }

    async function sendMessageToActiveChat(text: string, imageUrl?: string): Promise<string> {
        if (!activeChatId) return ""
        setIsLoading(true)

        const userMsg: Message = { role: "user", text, timestamp: new Date().toISOString() }
        addMessage(activeChatId, userMsg)

        await fetch(`${API_BASE}/conversations/${activeChatId}/messages`, {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({ content: text, attachment_url: imageUrl ?? null, system_generated: false }),
        })

        const chatId = activeChatId
        addMessage(chatId, { role: "assistant", text: "", timestamp: new Date().toISOString() })

        const res = await fetch(`${API_BASE}/chat/stream`, {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({
                message: text,
                producer_id: getProducerId(),
                image_url: imageUrl ?? null,
                crop_type: "general",
                province_state: provinceState,
                country: country,
                producer_type: 1,
                language: language,
                lat: null,
                lon: null,
                conversation_id: activeChatId,
            }),
        })

        const reader = res.body!.getReader()
        const decoder = new TextDecoder()
        let fullText = ""

        while (true) {
            const { done, value } = await reader.read()
            if (done) break
            const raw = decoder.decode(value, { stream: true })
            for (const line of raw.split("\n")) {
                if (!line.startsWith("data: ")) continue
                const chunk = line.slice(6)
                if (chunk === "[DONE]") break
                fullText += chunk
                updateLastAssistantMessage(chatId, fullText)
            }
        }

        await fetch(`${API_BASE}/conversations/${chatId}/messages`, {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({ content: fullText, system_generated: true }),
        })

        setIsLoading(false)
        return fullText
    }

    async function selectChat(chatId: string) {
        await AsyncStorage.setItem("active_chat_id", chatId)
        setActiveChatId(chatId)
        const alreadyLoaded = chats.find(c => c.id === chatId)?.messages.length ?? 0
        if (alreadyLoaded === 0) {
            const messages = await fetchMessages(chatId)
            setChats(prev => prev.map(c => c.id === chatId ? { ...c, messages } : c))
        }
    }

    return { chats, activeChatId, createChat, setActiveChatId: selectChat, sendMessageToActiveChat, isLoading, deleteChat }
}
