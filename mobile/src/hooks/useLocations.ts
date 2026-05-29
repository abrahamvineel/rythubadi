import { useState, useEffect, useCallback } from "react"
import { API_BASE } from "../constants/api"

export type FarmLocation = {
    id: string
    name: string
    latitude: number
    longitude: number
    producer_types: string[]
}

type CreateLocationData = {
    name: string
    latitude: number
    longitude: number
    producer_types: string[]
}

export function useLocations(token: string | null) {
    const [locations, setLocations] = useState<FarmLocation[]>([])
    const [loaded, setLoaded] = useState(false)

    function authHeaders() {
        return { "Content-Type": "application/json", Authorization: `Bearer ${token}` }
    }

    const load = useCallback(async () => {
        if (!token) return
        try {
            const res = await fetch(`${API_BASE}/locations`, { headers: authHeaders() })
            if (!res.ok) return
            const data = await res.json()
            setLocations(data)
        } catch {}
        finally { setLoaded(true) }
    }, [token])

    useEffect(() => { load() }, [load])

    async function addLocation(data: CreateLocationData): Promise<FarmLocation | null> {
        try {
            const res = await fetch(`${API_BASE}/locations`, {
                method: "POST",
                headers: authHeaders(),
                body: JSON.stringify(data),
            })
            if (!res.ok) return null
            const created: FarmLocation = await res.json()
            setLocations(prev => [...prev, created])
            return created
        } catch { return null }
    }

    async function removeLocation(id: string): Promise<boolean> {
        try {
            const res = await fetch(`${API_BASE}/locations/${id}`, {
                method: "DELETE",
                headers: authHeaders(),
            })
            if (!res.ok) return false
            setLocations(prev => prev.filter(l => l.id !== id))
            return true
        } catch { return false }
    }

    return { locations, loaded, addLocation, removeLocation, reload: load }
}
