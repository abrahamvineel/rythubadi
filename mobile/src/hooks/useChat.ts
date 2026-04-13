import { useState } from "react";

const API_BASE = "http://localhost:8000";

export type Message = {
    role: "user" | "assistant"
    text: string
}

export function useChat() {
    const [messages, setMessages] = useState<Message[]>([])
    const [isLoading, setIsLoading] = useState(false)

    async function sendMessage(text: string, imageUrl?: string): Promise<void> {
        const userMessage: Message = { role: "user", text }
        setMessages(prev => [...prev, userMessage])
        setIsLoading(true)

        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: text,
                producer_id: "test-farmer-1",
                image_url: imageUrl ?? null,
            }),
        })

        const data = await res.json()
        const assistantMessage: Message = { role: "assistant", text: data.specialist_response }
        setMessages(prev => [...prev, assistantMessage])
        setIsLoading(false)
    }

    return { messages, isLoading, sendMessage }
}
