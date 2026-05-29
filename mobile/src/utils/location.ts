import * as Location from "expo-location"

const LOCATION_TIMEOUT_MS = 12_000

/**
 * Returns the device's current farm location.
 *
 * Fast path: reads the OS-cached last-known position (instant, no satellite
 * wait). Accepts positions up to 5 minutes old and within 5 km accuracy —
 * more than good enough for farm pinning.
 *
 * Slow path: if no cached fix exists, requests a fresh one at the lowest
 * accuracy setting (cell towers + WiFi, not GPS satellites) and races it
 * against a 12-second timeout so the spinner can never hang forever.
 *
 * Throws on timeout or hardware failure — callers must catch.
 */
export async function getFarmLocation(): Promise<Location.LocationObject> {
    // ── Fast path ────────────────────────────────────────────────────────────
    const last = await Location.getLastKnownPositionAsync({
        maxAge: 5 * 60 * 1000,   // accept a fix from the last 5 minutes
        requiredAccuracy: 5000,   // within 5 km (fine for farm pinning)
    })
    if (last) return last

    // ── Slow path — raced against a hard deadline ────────────────────────────
    const fresh = Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.Lowest,   // cell/WiFi — resolves in seconds
    })
    const timeout = new Promise<never>((_, reject) =>
        setTimeout(
            () => reject(new Error("Location timed out after 12 s")),
            LOCATION_TIMEOUT_MS,
        )
    )
    return Promise.race([fresh, timeout])
}
