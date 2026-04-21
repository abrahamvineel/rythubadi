import { useState, useEffect } from "react"

const API_BASE = "http://localhost:8000"

function decodeToken(token: string): { user_id: string; name: string; language: string; province_state: string; country: string } | null {
    try {
        const payload = token.split(".")[1]
        return JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")))
    } catch {
        return null
    }
}

export function useAuth() {
    const [token, setToken] = useState<string | null>(null)
    const [name, setName] = useState<string | null>(null)
    const [language, setLanguage] = useState<string>("EN")
    const [provinceState, setProvinceState] = useState<string>("general")
    const [country, setCountry] = useState<string>("CA")
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const stored = localStorage.getItem("access_token")
        if (stored) {
            const decoded = decodeToken(stored)
            setToken(stored)
            setName(decoded?.name ?? null)
            setLanguage(decoded?.language ?? "EN")
            setProvinceState(decoded?.province_state ?? "general")
            setCountry(decoded?.country ?? "CA")
        }
        setLoading(false)
    }, [])

    async function register(email: string, name: string, password: string, language: string = "EN", provinceState: string = "general"): Promise<boolean> {
        setError(null)
        try {
            const res = await fetch(`${API_BASE}/auth/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, name, password, language, province_state: provinceState, country: "CA" }),
            })
            if (res.status === 409) { setError("Account already exists"); return false }
            if (!res.ok) { setError("Registration failed"); return false }
            const data = await res.json()
            const decoded = decodeToken(data.access_token)
            localStorage.setItem("access_token", data.access_token)
            setToken(data.access_token)
            setName(decoded?.name ?? null)
            setLanguage(decoded?.language ?? "EN")
            setProvinceState(decoded?.province_state ?? "general")
            setCountry(decoded?.country ?? "CA")
            return true
        } catch {
            setError("Could not reach server")
            return false
        }
    }

    async function login(email: string, password: string): Promise<boolean> {
        setError(null)
        try {
            const res = await fetch(`${API_BASE}/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            })
            if (res.status === 401) { setError("Invalid credentials"); return false }
            if (!res.ok) { setError("Login failed"); return false }
            const data = await res.json()
            const decoded = decodeToken(data.access_token)
            localStorage.setItem("access_token", data.access_token)
            setToken(data.access_token)
            setName(decoded?.name ?? null)
            setLanguage(decoded?.language ?? "EN")
            setProvinceState(decoded?.province_state ?? "general")
            setCountry(decoded?.country ?? "CA")
            return true
        } catch {
            setError("Could not reach server")
            return false
        }
    }

    function logout() {
        localStorage.removeItem("access_token")
        setToken(null)
        setName(null)
        setLanguage("EN")
        setProvinceState("general")
        setCountry("CA")
    }

    return { token, name, language, provinceState, country, loading, error, register, login, logout }
}
