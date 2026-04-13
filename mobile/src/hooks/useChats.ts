import { useState } from "react";
import { Message } from './useChat';

export type Chat = {
    id: string
    title: string
    messages: Message[]
}

export function useChats() {
    const [chats, setChats] = useState<Chat[]>([])
    const [activeChatId, setActiveChatId] = useState<string | null>(null)

    function createChat(): string {
        const id = Date.now().toString()
        const newChat: Chat = { id, title: "New conversation", messages: [] }
        setChats(prev => [...prev, newChat])
        setActiveChatId(id)
        return id
    }

    function addMessage(chatId: string, message: Message) {
        setChats(prev => prev.map(
            chat => chat.id === chatId ? 
            { ...chat, messages: [...chat.messages, message]}
            : chat
        ))
    }

    async function sendMessageToActiveChat(text: string): Promise<void> {
        if (!activeChatId) return
        const userMsg: Message = { role: "user", text }
        addMessage(activeChatId, userMsg)

        const res = await fetch("http://localhost:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: text,
                producer_id: "test-farmer-1",
                image_url: null,
            }),
        })
        const data = await res.json()
        const assistantMsg: Message = { role: "assistant", text: data.specialist_response }
        addMessage(activeChatId, assistantMsg)
    }
    return { chats, activeChatId, createChat, setActiveChatId, sendMessageToActiveChat }
}