import { useState } from "react";

const API_BASE = "http://localhost:8000";

export function useChat() {

    const [response, setResponse] = useState("");

    const [isLoading, setIsLoading] = useState(false);

    async function sendMessage(text: string, imageUrl?: string): Promise<void> {
        
        setIsLoading(true);

        const res = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                message: text,
                producer_id: "test-farmer-1",
                image_url: imageUrl ?? null,
            }),
        });

        const data = await res.json();
        setResponse(data.specialist_response);
        setIsLoading(false);
    }
    return { response, isLoading, sendMessage };
}