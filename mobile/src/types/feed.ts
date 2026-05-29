export type FeedSeverity = "info" | "warning" | "alert"

/**
 * Known subject types — exported as a const so the codebase has one source of truth
 * for string values, but FeedEvent.subject_type is typed as `string | null` so
 * new entity types added to the backend require zero frontend type changes.
 *
 * Add a new entry here when a new navigable entity type is introduced:
 *   VALVE: "valve"
 *   BATCH: "batch"
 *   ZONE:  "zone"
 */
export const FeedSubjectTypes = {
    ANIMAL:   "animal",
    LOCATION: "location",
    ZONE:     "zone",
    VALVE:    "valve",
    BATCH:    "batch",
} as const

export type FeedEvent = {
    id: string
    severity: FeedSeverity
    agent: string           // e.g. "CropAdvisorAgent", "CattleAdvisorAgent"
    agent_emoji: string     // e.g. "🌾", "🐄", "🐔"
    title: string
    body: string
    created_at: string      // ISO 8601
    location_id: string | null   // context anchor — used for filtering by farm
    // ── Generic subject reference ─────────────────────────────────────────────
    // Replaces entity-specific fields (animal_id, field_id, zone_id, etc.).
    // subject_type tells the UI which Monitor sub-screen to navigate to.
    // subject_id is the ID of that entity in its own table.
    // subject_name is denormalized here so reads never require a join.
    subject_type: string | null  // use FeedSubjectTypes constants
    subject_id: string | null
    subject_name: string | null
    // ─────────────────────────────────────────────────────────────────────────
    reply_count: number
}
