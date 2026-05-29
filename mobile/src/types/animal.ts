export type AnimalStatus = "healthy" | "watch" | "alert"

export type SensorReading = {
    value: number
    unit: string
    recorded_at: string     // ISO 8601
}

export type SensorCard = {
    id: string
    sensor_type: string     // e.g. "temperature", "heart_rate", "weight"
    label: string
    current: SensorReading
    history: number[]       // last N readings for sparkline (oldest → newest)
    status: AnimalStatus
    threshold_low: number | null
    threshold_high: number | null
}

export type Animal = {
    id: string
    name: string
    species: string         // "cattle" | "poultry" | "goat" | etc.
    tag: string             // ear tag or band ID, e.g. "#CA-0042"
    location_id: string
    status: AnimalStatus    // derived from worst sensor status
    sensors: SensorCard[]
}
