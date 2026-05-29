/**
 * useThread — manages a persistent conversation thread tied to a single feed event.
 *
 * Architecture decision:
 *   Each feed event gets its own conversation (via POST /conversations) the first time
 *   the user opens its thread.  The conversation ID is persisted in AsyncStorage so
 *   subsequent opens resume the same thread rather than starting over.
 *
 * Context injection:
 *   The very first message the farmer sends is prefixed with the feed event's title and
 *   body.  This gives the LLM all the context it needs without the farmer having to
 *   repeat the alert.  Subsequent messages in the same conversation are sent as-is —
 *   the history already carries the context.
 */
import { useState, useEffect, useCallback, useRef } from "react"
import AsyncStorage from "@react-native-async-storage/async-storage"
import { API_BASE } from "../constants/api"
import { Message } from "./useChat"
import { decodeToken } from "../utils/token"
import { FeedEvent } from "../types/feed"

export function useThread(
    token: string | null,
    event: FeedEvent | null,
    language: string = "EN",
    country: string = "CA",
) {
    const [conversationId, setConversationId] = useState<string | null>(null)
    const [messages, setMessages] = useState<Message[]>([])
    const [isLoading, setIsLoading] = useState(false)
    const [isInitialising, setIsInitialising] = useState(false)
    // Tracks whether the next send is the very first message in this thread
    const isFirstMessage = useRef(true)

    function authHeaders(): HeadersInit {
        return { "Content-Type": "application/json", Authorization: `Bearer ${token}` }
    }

    function getProducerId(): string {
        if (!token) return ""
        return decodeToken(token)?.user_id ?? ""
    }

    const initialise = useCallback(async () => {
        if (!token || !event) return
        setIsInitialising(true)
        try {
            const storageKey = `thread_conv_${event.id}`
            const existingId = await AsyncStorage.getItem(storageKey)

            if (existingId) {
                // Resume an existing thread: load its messages
                setConversationId(existingId)
                const res = await fetch(
                    `${API_BASE}/conversations/${existingId}/messages`,
                    { headers: authHeaders() },
                )
                if (res.ok) {
                    const data = await res.json()
                    const loaded: Message[] = data.map(
                        (m: { content: string; system_generated: boolean }) => ({
                            role: m.system_generated ? "assistant" : "user",
                            text: m.content,
                            timestamp: new Date().toISOString(),
                        }),
                    )
                    setMessages(loaded)
                    isFirstMessage.current = loaded.length === 0
                } else {
                    isFirstMessage.current = true
                }
            } else {
                // First open: create a new conversation for this thread
                const res = await fetch(`${API_BASE}/conversations`, {
                    method: "POST",
                    headers: authHeaders(),
                    body: JSON.stringify({ title: `Thread: ${event.title}` }),
                })
                if (res.ok) {
                    const data = await res.json()
                    await AsyncStorage.setItem(storageKey, data.id)
                    setConversationId(data.id)
                    setMessages([])
                    isFirstMessage.current = true
                }
            }
        } catch {
            // Silently fail — the UI shows an empty thread and the user can still type
        } finally {
            setIsInitialising(false)
        }
    }, [token, event?.id])

    // Re-initialise whenever the event changes (i.e. user opens a different thread)
    useEffect(() => {
        setMessages([])
        setConversationId(null)
        isFirstMessage.current = true
        initialise()
    }, [initialise])

    function appendMessage(msg: Message) {
        setMessages(prev => [...prev, msg])
    }

    function updateLastAssistant(text: string) {
        setMessages(prev => {
            const arr = [...prev]
            const last = arr.length - 1
            if (last >= 0 && arr[last].role === "assistant") {
                arr[last] = { ...arr[last], text }
            }
            return arr
        })
    }

    async function send(userText: string): Promise<void> {
        if (!conversationId || !userText.trim() || isLoading) return
        setIsLoading(true)

        // On the first message only, prepend the feed event context so the LLM
        // knows what alert it's being asked about.
        const textToSend = isFirstMessage.current && event
            ? `[Farm alert — ${event.agent}: "${event.title}"]\n${event.body}\n\nFarmer question: ${userText}`
            : userText

        isFirstMessage.current = false

        // Show the original text (without the prefix) in the UI
        appendMessage({ role: "user", text: userText, timestamp: new Date().toISOString() })

        // Persist user message
        await fetch(`${API_BASE}/conversations/${conversationId}/messages`, {
            method: "POST",
            headers: authHeaders(),
            body: JSON.stringify({ content: textToSend, system_generated: false }),
        }).catch(() => {})

        // Placeholder assistant bubble for streaming
        appendMessage({ role: "assistant", text: "", timestamp: new Date().toISOString() })

        try {
            const res = await fetch(`${API_BASE}/chat/stream`, {
                method: "POST",
                headers: authHeaders(),
                body: JSON.stringify({
                    message: textToSend,
                    producer_id: getProducerId(),
                    image_url: null,
                    crop_type: "general",
                    province_state: "general",
                    country,
                    producer_type: 1,
                    language,
                    lat: null,
                    lon: null,
                    conversation_id: conversationId,
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
                    updateLastAssistant(fullText)
                }
            }

            // Persist assistant reply
            await fetch(`${API_BASE}/conversations/${conversationId}/messages`, {
                method: "POST",
                headers: authHeaders(),
                body: JSON.stringify({ content: fullText, system_generated: true }),
            }).catch(() => {})
        } catch {
            updateLastAssistant("Sorry, I couldn't reach the server. Please try again.")
        }

        setIsLoading(false)
    }

    return { messages, isLoading, isInitialising, send }
}
