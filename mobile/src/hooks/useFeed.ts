import { useState, useEffect, useCallback } from "react"
import { API_BASE } from "../constants/api"
import { FeedEvent, FeedSubjectTypes } from "../types/feed"

// Seed data for demo when backend has no /feed endpoint yet.
// Each event uses the generic subject_type / subject_id / subject_name fields.
const MOCK_EVENTS: FeedEvent[] = [
    {
        id: "mock-1",
        severity: "alert",
        agent: "CattleAdvisorAgent",
        agent_emoji: "🐄",
        title: "Low temperature detected — Bessie",
        body: "Body temperature dropped to 37.8°C (normal: 38.5–39.5°C). May indicate early-stage fever or environmental stress. Monitor closely and consider veterinary consultation if the temperature continues to fall.",
        created_at: new Date(Date.now() - 25 * 60 * 1000).toISOString(),
        location_id: "loc-1",
        subject_type: FeedSubjectTypes.ANIMAL,
        subject_id: "animal-1",
        subject_name: "Bessie",
        reply_count: 0,
    },
    {
        id: "mock-2",
        severity: "warning",
        agent: "CropAdvisorAgent",
        agent_emoji: "🌾",
        title: "Soil moisture below threshold — North Field",
        body: "Soil moisture reading at 18% — 12% below the optimal range for wheat at this growth stage. Risk of stress if no rain falls in the next 48 hours. Consider irrigation.",
        created_at: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
        location_id: "loc-1",
        subject_type: FeedSubjectTypes.LOCATION,
        subject_id: "loc-1",
        subject_name: "North Field",
        reply_count: 2,
    },
    {
        id: "mock-3",
        severity: "warning",
        agent: "CropAdvisorAgent",
        agent_emoji: "🌾",
        title: "pH out of range — Greenhouse Zone B",
        body: "Soil pH reading at 4.9 — below the optimal 6.0–7.0 for tomatoes. Prolonged acidity inhibits nutrient uptake. Consider applying garden lime to raise pH.",
        created_at: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
        location_id: "loc-2",
        subject_type: FeedSubjectTypes.ZONE,
        subject_id: "zone-1",
        subject_name: "Greenhouse Zone B",
        reply_count: 0,
    },
    {
        id: "mock-4",
        severity: "info",
        agent: "SchemeAdvisorAgent",
        agent_emoji: "📋",
        title: "New subsidy available — Ontario Grain Program",
        body: "Ontario Grain and Oilseed Support Program applications are open until June 30. Based on your wheat crop and acreage, you may be eligible for up to $4,200.",
        created_at: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(),
        location_id: null,
        subject_type: null,
        subject_id: null,
        subject_name: null,
        reply_count: 0,
    },
]

export function useFeed(token: string | null) {
    const [events, setEvents] = useState<FeedEvent[]>([])
    const [loading, setLoading] = useState(false)

    function authHeaders() {
        return { "Content-Type": "application/json", Authorization: `Bearer ${token}` }
    }

    const load = useCallback(async () => {
        if (!token) return
        setLoading(true)
        try {
            const res = await fetch(`${API_BASE}/feed`, { headers: authHeaders() })
            if (res.ok) {
                const data: FeedEvent[] = await res.json()
                setEvents(data.length > 0 ? data : MOCK_EVENTS)
            } else {
                setEvents(MOCK_EVENTS)
            }
        } catch {
            setEvents(MOCK_EVENTS)
        } finally {
            setLoading(false)
        }
    }, [token])

    useEffect(() => { load() }, [load])

    const unreadAlerts = events.filter(e => e.severity === "alert").length

    return { events, loading, unreadAlerts, reload: load }
}
