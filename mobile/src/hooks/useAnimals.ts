import { useState, useEffect, useCallback } from "react"
import { API_BASE } from "../constants/api"
import { Animal } from "../types/animal"

// Seed data used during development before the backend /animals endpoint exists.
// Remove once real data is flowing.
const MOCK_ANIMALS: Animal[] = [
    {
        id: "animal-1",
        name: "Bessie",
        species: "cattle",
        tag: "#CA-0042",
        location_id: "loc-1",
        status: "alert",
        sensors: [
            {
                id: "s1",
                sensor_type: "temperature",
                label: "Body Temp",
                current: { value: 37.8, unit: "°C", recorded_at: new Date().toISOString() },
                history: [39.1, 38.9, 38.7, 38.5, 38.2, 38.0, 37.8],
                status: "alert",
                threshold_low: 38.5,
                threshold_high: 39.5,
            },
            {
                id: "s2",
                sensor_type: "heart_rate",
                label: "Heart Rate",
                current: { value: 64, unit: "bpm", recorded_at: new Date().toISOString() },
                history: [62, 63, 65, 64, 63, 65, 64],
                status: "healthy",
                threshold_low: 48,
                threshold_high: 84,
            },
            {
                id: "s3",
                sensor_type: "weight",
                label: "Weight",
                current: { value: 482, unit: "kg", recorded_at: new Date().toISOString() },
                history: [480, 481, 481, 482, 483, 482, 482],
                status: "healthy",
                threshold_low: null,
                threshold_high: null,
            },
        ],
    },
    {
        id: "animal-2",
        name: "Daisy",
        species: "cattle",
        tag: "#CA-0043",
        location_id: "loc-1",
        status: "watch",
        sensors: [
            {
                id: "s4",
                sensor_type: "temperature",
                label: "Body Temp",
                current: { value: 39.2, unit: "°C", recorded_at: new Date().toISOString() },
                history: [38.8, 38.9, 39.0, 39.1, 39.1, 39.2, 39.2],
                status: "watch",
                threshold_low: 38.5,
                threshold_high: 39.5,
            },
            {
                id: "s5",
                sensor_type: "heart_rate",
                label: "Heart Rate",
                current: { value: 72, unit: "bpm", recorded_at: new Date().toISOString() },
                history: [68, 70, 71, 72, 71, 72, 72],
                status: "healthy",
                threshold_low: 48,
                threshold_high: 84,
            },
        ],
    },
    {
        id: "animal-3",
        name: "Hen-A03",
        species: "poultry",
        tag: "#PO-0003",
        location_id: "loc-1",
        status: "healthy",
        sensors: [
            {
                id: "s6",
                sensor_type: "temperature",
                label: "Shed Temp",
                current: { value: 21.5, unit: "°C", recorded_at: new Date().toISOString() },
                history: [21.0, 21.2, 21.3, 21.4, 21.4, 21.5, 21.5],
                status: "healthy",
                threshold_low: 18.0,
                threshold_high: 25.0,
            },
            {
                id: "s7",
                sensor_type: "humidity",
                label: "Humidity",
                current: { value: 62, unit: "%", recorded_at: new Date().toISOString() },
                history: [60, 61, 62, 63, 62, 62, 62],
                status: "healthy",
                threshold_low: 50,
                threshold_high: 70,
            },
        ],
    },
]

export function useAnimals(token: string | null, locationId: string | null) {
    const [animals, setAnimals] = useState<Animal[]>([])
    const [loading, setLoading] = useState(false)

    function authHeaders() {
        return { "Content-Type": "application/json", Authorization: `Bearer ${token}` }
    }

    const load = useCallback(async () => {
        if (!token) return
        setLoading(true)
        try {
            const params = locationId ? `?location_id=${locationId}` : ""
            const res = await fetch(`${API_BASE}/animals${params}`, { headers: authHeaders() })
            if (res.ok) {
                const data: Animal[] = await res.json()
                setAnimals(data.length > 0 ? data : MOCK_ANIMALS)
            } else {
                setAnimals(MOCK_ANIMALS)
            }
        } catch {
            setAnimals(MOCK_ANIMALS)
        } finally {
            setLoading(false)
        }
    }, [token, locationId])

    useEffect(() => { load() }, [load])

    return { animals, loading, reload: load }
}
