/**
 * MonitorScreen — three-level drill-down:
 *   Overview (location cards) → Herd (animal list) → Animal detail (sensor cards + sparklines)
 *
 * Deep-linking from Feed:
 *   The `target` prop carries a subject_type + subject_id from a tapped feed card.
 *   MonitorScreen processes it once and navigates to the right sub-screen automatically.
 *   A `processedTargetId` ref prevents the same target being re-processed on re-renders.
 *
 * Navigation is managed with local state — no external navigator — so the TabBar
 * remains visible throughout all three levels.
 */
import React, { useState, useEffect, useRef } from "react"
import {
    View,
    Text,
    ScrollView,
    StyleSheet,
    TouchableOpacity,
    ActivityIndicator,
    useWindowDimensions,
} from "react-native"
import { useSafeAreaInsets } from "react-native-safe-area-context"

const DESKTOP_BREAKPOINT = 768
import { useLocations } from "../hooks/useLocations"
import { useAnimals } from "../hooks/useAnimals"
import { Animal, AnimalStatus, SensorCard } from "../types/animal"
import { FeedSubjectTypes } from "../types/feed"

type MonitorView = "overview" | "herd" | "animal"

/**
 * MonitorTarget — passed from App.tsx when the farmer taps "View <entity>" on a feed card.
 * Exported so App.tsx can import the type without a circular dependency.
 */
export type MonitorTarget = {
    subjectType: string
    subjectId: string
    locationId: string | null   // needed to load the right animal list for ANIMAL targets
}

type Props = {
    token: string | null
    target?: MonitorTarget | null
}

// ─── Status helpers ────────────────────────────────────────────────────────────

const STATUS_COLOR: Record<AnimalStatus, string> = {
    healthy: "#4CAF50",
    watch:   "#FF9800",
    alert:   "#F44336",
}

const STATUS_EMOJI: Record<AnimalStatus, string> = {
    healthy: "✅",
    watch:   "⚠️",
    alert:   "🚨",
}

const SPECIES_EMOJI: Record<string, string> = {
    cattle:  "🐄",
    poultry: "🐔",
    goat:    "🐐",
    sheep:   "🐑",
}

// ─── Sparkline ─────────────────────────────────────────────────────────────────

function Sparkline({ values, status }: { values: number[]; status: AnimalStatus }) {
    if (values.length === 0) return null
    const min = Math.min(...values)
    const max = Math.max(...values)
    const range = max - min || 1

    return (
        <View style={spark.row}>
            {values.map((v, i) => {
                const pct = (v - min) / range
                const h = pct * 28 + 4
                return (
                    <View
                        key={i}
                        style={[spark.bar, {
                            height: h,
                            backgroundColor: i === values.length - 1 ? STATUS_COLOR[status] : "#C8E6C9",
                        }]}
                    />
                )
            })}
        </View>
    )
}

const spark = StyleSheet.create({
    row: { flexDirection: "row", alignItems: "flex-end", gap: 2, height: 36 },
    bar: { width: 9, borderRadius: 3, minHeight: 4 },
})

// ─── SensorCard ────────────────────────────────────────────────────────────────

function SensorCardView({ sensor }: { sensor: SensorCard }) {
    const color = STATUS_COLOR[sensor.status]
    return (
        <View style={[mon.sensorCard, { borderLeftColor: color }]}>
            <View style={mon.sensorTop}>
                <Text style={mon.sensorLabel}>{sensor.label.toUpperCase()}</Text>
                <Text style={{ fontSize: 16 }}>{STATUS_EMOJI[sensor.status]}</Text>
            </View>
            <Text style={[mon.sensorValue, { color }]}>
                {sensor.current.value}
                <Text style={mon.sensorUnit}> {sensor.current.unit}</Text>
            </Text>
            {sensor.threshold_low !== null && sensor.threshold_high !== null && (
                <Text style={mon.sensorRange}>
                    Normal: {sensor.threshold_low}–{sensor.threshold_high} {sensor.current.unit}
                </Text>
            )}
            <Sparkline values={sensor.history} status={sensor.status} />
        </View>
    )
}

// ─── Main screen ───────────────────────────────────────────────────────────────

export function MonitorScreen({ token, target }: Props) {
    const insets = useSafeAreaInsets()
    const { width } = useWindowDimensions()
    const isDesktop = width >= DESKTOP_BREAKPOINT
    const { locations, loaded: locsLoaded } = useLocations(token)

    const [view, setView] = useState<MonitorView>("overview")
    const [selectedLocationId, setSelectedLocationId] = useState<string | null>(null)
    const [selectedAnimal, setSelectedAnimal] = useState<Animal | null>(null)
    const [speciesFilter, setSpeciesFilter] = useState<string>("all")

    const { animals, loading: animalsLoading } = useAnimals(token, selectedLocationId)

    // Prevent the same target from being processed more than once
    const processedTargetId = useRef<string | null>(null)

    // ── Deep-link from Feed ────────────────────────────────────────────────────
    // Step 1: when a new target arrives, navigate to the right location/herd
    useEffect(() => {
        if (!target || target.subjectId === processedTargetId.current) return
        processedTargetId.current = target.subjectId

        if (target.subjectType === FeedSubjectTypes.LOCATION || target.subjectType === FeedSubjectTypes.ZONE) {
            // Navigate directly to herd view for this location
            const locationId = target.subjectId
            setSelectedLocationId(locationId)
            setSpeciesFilter("all")
            setSelectedAnimal(null)
            setView("herd")
        } else if (target.subjectType === FeedSubjectTypes.ANIMAL && target.locationId) {
            // First load the herd for the animal's location;
            // Step 2 (below) will pick up when animals load and navigate to the specific animal
            setSelectedLocationId(target.locationId)
            setSpeciesFilter("all")
            setSelectedAnimal(null)
            setView("herd")
        }
        // Unknown subject types: stay on overview — future types handled by adding a case above
    }, [target])

    // Step 2 (ANIMAL only): once the herd is loaded, find and open the target animal
    useEffect(() => {
        if (!target || target.subjectType !== FeedSubjectTypes.ANIMAL) return
        if (target.subjectId === processedTargetId.current && selectedAnimal) return
        if (animals.length === 0) return

        const animal = animals.find(a => a.id === target.subjectId)
        if (animal) {
            setSelectedAnimal(animal)
            setView("animal")
        }
    }, [animals, target])

    // ── Navigation helpers ─────────────────────────────────────────────────────

    function goToHerd(locationId: string) {
        setSelectedLocationId(locationId)
        setSpeciesFilter("all")
        setView("herd")
    }

    function goToAnimal(animal: Animal) {
        setSelectedAnimal(animal)
        setView("animal")
    }

    function goBack() {
        if (view === "animal") { setSelectedAnimal(null); setView("herd") }
        else if (view === "herd") { setSelectedLocationId(null); setView("overview") }
    }

    // ── Derived values ─────────────────────────────────────────────────────────

    const filteredAnimals = speciesFilter === "all"
        ? animals
        : animals.filter(a => a.species === speciesFilter)

    const uniqueSpecies = Array.from(new Set(animals.map(a => a.species)))
    const selectedLocation = locations.find(l => l.id === selectedLocationId)

    const healthy  = animals.filter(a => a.status === "healthy").length
    const watching = animals.filter(a => a.status === "watch").length
    const alerting = animals.filter(a => a.status === "alert").length

    const headerTitle =
        view === "overview" ? "Monitor"
        : view === "herd"   ? (selectedLocation?.name ?? "Herd")
        :                     (selectedAnimal?.name ?? "Animal")

    const headerSub =
        view === "overview" ? `${locations.length} location${locations.length !== 1 ? "s" : ""}`
        : view === "herd"   ? `${animals.length} animal${animals.length !== 1 ? "s" : ""}`
        :                     `${selectedAnimal?.tag ?? ""} · ${selectedAnimal?.species ?? ""}`

    return (
        <View style={[mon.root, { paddingTop: insets.top }]}>
            {/* ── Header ── */}
            <View style={[mon.header, isDesktop && mon.headerDesktop]}>
                {view !== "overview" && (
                    <TouchableOpacity
                        onPress={goBack}
                        style={mon.backBtn}
                        hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
                    >
                        <Text style={[mon.backText, isDesktop && mon.backTextDesktop]}>← Back</Text>
                    </TouchableOpacity>
                )}
                <View style={{ flex: 1 }}>
                    <Text style={[mon.headerTitle, isDesktop && mon.headerTitleDesktop]}>{headerTitle}</Text>
                    <Text style={[mon.headerSub, isDesktop && mon.headerSubDesktop]}>{headerSub}</Text>
                </View>
            </View>

            {/* ── Overview ── */}
            {view === "overview" && (
                <ScrollView
                    style={{ flex: 1 }}
                    contentContainerStyle={mon.listContent}
                    showsVerticalScrollIndicator={false}
                >
                    {!locsLoaded && (
                        <View style={mon.center}>
                            <ActivityIndicator color="#4CAF50" size="large" />
                        </View>
                    )}

                    {locsLoaded && locations.length === 0 && (
                        <View style={mon.emptyState}>
                            <Text style={mon.emptyEmoji}>📡</Text>
                            <Text style={mon.emptyTitle}>No locations yet</Text>
                            <Text style={mon.emptySub}>
                                Pin your farm locations in your profile to start{"\n"}monitoring crops and livestock.
                            </Text>
                        </View>
                    )}

                    {locations.map(loc => (
                        <TouchableOpacity
                            key={loc.id}
                            style={mon.locationCard}
                            onPress={() => goToHerd(loc.id)}
                            activeOpacity={0.8}
                        >
                            <View style={mon.locationHeader}>
                                <Text style={mon.locationEmoji}>📍</Text>
                                <View style={{ flex: 1 }}>
                                    <Text style={mon.locationName}>{loc.name}</Text>
                                    <Text style={mon.locationTypes}>
                                        {loc.producer_types.join(" · ")}
                                    </Text>
                                </View>
                                <Text style={mon.chevron}>›</Text>
                            </View>
                            <View style={mon.statRow}>
                                {[
                                    { label: "Healthy", color: "#4CAF50", bg: "#E8F5E9" },
                                    { label: "Watch",   color: "#E65100", bg: "#FFF3E0" },
                                    { label: "Alert",   color: "#B71C1C", bg: "#FFEBEE" },
                                ].map(s => (
                                    <View key={s.label} style={[mon.statPill, { backgroundColor: s.bg }]}>
                                        <Text style={[mon.statText, { color: s.color }]}>{s.label}</Text>
                                    </View>
                                ))}
                            </View>
                        </TouchableOpacity>
                    ))}
                </ScrollView>
            )}

            {/* ── Herd view ── */}
            {view === "herd" && (
                <View style={{ flex: 1 }}>
                    <View style={mon.summaryStrip}>
                        {[
                            { count: healthy,  label: "Healthy", color: "#4CAF50" },
                            { count: watching, label: "Watch",   color: "#FF9800" },
                            { count: alerting, label: "Alert",   color: "#F44336" },
                        ].map((item, i) => (
                            <React.Fragment key={item.label}>
                                {i > 0 && <View style={mon.stripSep} />}
                                <View style={mon.summaryItem}>
                                    <Text style={[mon.summaryCount, { color: item.color }]}>
                                        {item.count}
                                    </Text>
                                    <Text style={mon.summaryLabel}>{item.label}</Text>
                                </View>
                            </React.Fragment>
                        ))}
                    </View>

                    {uniqueSpecies.length > 1 && (
                        <ScrollView
                            horizontal
                            showsHorizontalScrollIndicator={false}
                            contentContainerStyle={mon.filterRow}
                            style={mon.filterScrollView}
                        >
                            {["all", ...uniqueSpecies].map(s => (
                                <TouchableOpacity
                                    key={s}
                                    style={[mon.filterChip, speciesFilter === s && mon.filterChipActive]}
                                    onPress={() => setSpeciesFilter(s)}
                                >
                                    <Text style={[mon.filterText, speciesFilter === s && mon.filterTextActive]}>
                                        {s === "all" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)}
                                    </Text>
                                </TouchableOpacity>
                            ))}
                        </ScrollView>
                    )}

                    {animalsLoading ? (
                        <View style={mon.center}>
                            <ActivityIndicator color="#4CAF50" size="large" />
                        </View>
                    ) : (
                        <ScrollView
                            style={{ flex: 1 }}
                            contentContainerStyle={mon.listContent}
                            showsVerticalScrollIndicator={false}
                        >
                            {filteredAnimals.map(animal => (
                                <TouchableOpacity
                                    key={animal.id}
                                    style={[mon.animalCard, { borderLeftColor: STATUS_COLOR[animal.status] }]}
                                    onPress={() => goToAnimal(animal)}
                                    activeOpacity={0.8}
                                >
                                    <View style={mon.animalRow}>
                                        <Text style={mon.animalEmoji}>
                                            {SPECIES_EMOJI[animal.species] ?? "🐾"}
                                        </Text>
                                        <View style={{ flex: 1 }}>
                                            <Text style={mon.animalName}>{animal.name}</Text>
                                            <Text style={mon.animalTag}>{animal.tag}</Text>
                                        </View>
                                        <Text style={{ fontSize: 18, marginRight: 4 }}>
                                            {STATUS_EMOJI[animal.status]}
                                        </Text>
                                        <Text style={mon.chevron}>›</Text>
                                    </View>
                                    {animal.sensors.length > 0 && (
                                        <View style={mon.sensorPreviewRow}>
                                            {animal.sensors.slice(0, 3).map(s => (
                                                <View key={s.id} style={mon.sensorPreview}>
                                                    <Text style={mon.previewLabel}>{s.label}</Text>
                                                    <Text style={[mon.previewVal, { color: STATUS_COLOR[s.status] }]}>
                                                        {s.current.value}{s.current.unit}
                                                    </Text>
                                                </View>
                                            ))}
                                        </View>
                                    )}
                                </TouchableOpacity>
                            ))}
                        </ScrollView>
                    )}
                </View>
            )}

            {/* ── Animal detail ── */}
            {view === "animal" && selectedAnimal && (
                <ScrollView
                    style={{ flex: 1 }}
                    contentContainerStyle={mon.listContent}
                    showsVerticalScrollIndicator={false}
                >
                    <View style={[mon.detailCard, { borderColor: STATUS_COLOR[selectedAnimal.status] }]}>
                        <Text style={mon.detailEmoji}>
                            {SPECIES_EMOJI[selectedAnimal.species] ?? "🐾"}
                        </Text>
                        <Text style={mon.detailName}>{selectedAnimal.name}</Text>
                        <Text style={mon.detailTag}>{selectedAnimal.tag}</Text>
                        <View style={[mon.statusBadge, { backgroundColor: STATUS_COLOR[selectedAnimal.status] }]}>
                            <Text style={mon.statusBadgeText}>
                                {selectedAnimal.status.toUpperCase()}
                            </Text>
                        </View>
                    </View>

                    <Text style={mon.sectionTitle}>Live Sensors</Text>

                    {selectedAnimal.sensors.map(sensor => (
                        <SensorCardView key={sensor.id} sensor={sensor} />
                    ))}
                </ScrollView>
            )}
        </View>
    )
}

const mon = StyleSheet.create({
    root: { flex: 1, backgroundColor: "#F4F9F4" },

    header: {
        flexDirection: "row",
        alignItems: "center",
        paddingHorizontal: 20,
        paddingVertical: 14,
        backgroundColor: "#1B5E20",
        gap: 12,
    },
    headerDesktop: {
        backgroundColor: "#F4F9F4",
        paddingVertical: 16,
        borderBottomWidth: 1,
        borderBottomColor: "#D8EDD8",
    },
    backBtn: { paddingRight: 4 },
    backText: { color: "#A5D6A7", fontSize: 14, fontWeight: "600" },
    backTextDesktop: { color: "#2E7D32" },
    headerTitle: { fontSize: 20, fontWeight: "700", color: "#FFFFFF" },
    headerTitleDesktop: { fontSize: 22, color: "#1B5E20" },
    headerSub: { fontSize: 12, color: "#A5D6A7", marginTop: 2 },
    headerSubDesktop: { color: "#7A9E7A" },

    listContent: { padding: 16, gap: 12, paddingBottom: 24 },
    center: { flex: 1, alignItems: "center", justifyContent: "center", marginTop: 60 },

    emptyState: { alignItems: "center", marginTop: 60, gap: 12, paddingHorizontal: 24 },
    emptyEmoji: { fontSize: 52 },
    emptyTitle: { fontSize: 18, fontWeight: "700", color: "#2E7D32" },
    emptySub: { fontSize: 14, color: "#7A9E7A", textAlign: "center", lineHeight: 21 },

    locationCard: {
        backgroundColor: "#FFFFFF", borderRadius: 14, padding: 14, gap: 10,
        shadowColor: "#000", shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.06, shadowRadius: 3, elevation: 2,
    },
    locationHeader: { flexDirection: "row", alignItems: "center", gap: 10 },
    locationEmoji: { fontSize: 20 },
    locationName: { fontSize: 15, fontWeight: "700", color: "#1A3A1A" },
    locationTypes: { fontSize: 11, color: "#7A9E7A", marginTop: 2 },
    chevron: { fontSize: 22, color: "#A5D6A7" },
    statRow: { flexDirection: "row", gap: 6 },
    statPill: { borderRadius: 8, paddingHorizontal: 10, paddingVertical: 4 },
    statText: { fontSize: 11, fontWeight: "700" },

    summaryStrip: {
        flexDirection: "row", backgroundColor: "#FFFFFF",
        borderBottomWidth: 1, borderBottomColor: "#D8EDD8", paddingVertical: 12,
    },
    summaryItem: { flex: 1, alignItems: "center", gap: 2 },
    summaryCount: { fontSize: 24, fontWeight: "700" },
    summaryLabel: { fontSize: 11, color: "#7A9E7A" },
    stripSep: { width: 1, backgroundColor: "#D8EDD8", marginVertical: 8 },

    filterScrollView: { flexGrow: 0, flexShrink: 0 },
    filterRow: { flexDirection: "row", alignItems: "center", paddingHorizontal: 16, paddingVertical: 8, gap: 8 },
    filterChip: {
        paddingHorizontal: 14, paddingVertical: 6, borderRadius: 16,
        backgroundColor: "#F0F7F0", borderWidth: 1, borderColor: "#C8E6C9",
    },
    filterChipActive: { backgroundColor: "#2E7D32", borderColor: "#2E7D32" },
    filterText: { fontSize: 13, color: "#7A9E7A", fontWeight: "500" },
    filterTextActive: { color: "#FFFFFF", fontWeight: "700" },

    animalCard: {
        backgroundColor: "#FFFFFF", borderRadius: 12, borderLeftWidth: 4, padding: 12, gap: 8,
        shadowColor: "#000", shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
    },
    animalRow: { flexDirection: "row", alignItems: "center", gap: 10 },
    animalEmoji: { fontSize: 24 },
    animalName: { fontSize: 14, fontWeight: "700", color: "#1A3A1A" },
    animalTag: { fontSize: 11, color: "#7A9E7A", marginTop: 2 },
    sensorPreviewRow: { flexDirection: "row", gap: 16, marginTop: 2 },
    sensorPreview: { gap: 1 },
    previewLabel: { fontSize: 10, color: "#7A9E7A" },
    previewVal: { fontSize: 13, fontWeight: "700" },

    detailCard: {
        backgroundColor: "#FFFFFF", borderRadius: 16, borderWidth: 2, padding: 24,
        alignItems: "center", gap: 6,
    },
    detailEmoji: { fontSize: 44 },
    detailName: { fontSize: 22, fontWeight: "700", color: "#1A3A1A" },
    detailTag: { fontSize: 13, color: "#7A9E7A" },
    statusBadge: { borderRadius: 12, paddingHorizontal: 16, paddingVertical: 5, marginTop: 4 },
    statusBadgeText: { color: "#FFFFFF", fontWeight: "700", fontSize: 12, letterSpacing: 0.8 },

    sectionTitle: {
        fontSize: 11, fontWeight: "700", color: "#2E7D32",
        textTransform: "uppercase", letterSpacing: 1, marginTop: 4, marginBottom: -4,
    },
    sensorCard: {
        backgroundColor: "#FFFFFF", borderRadius: 12, borderLeftWidth: 4, padding: 14, gap: 4,
        shadowColor: "#000", shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
    },
    sensorTop: { flexDirection: "row", alignItems: "center", justifyContent: "space-between" },
    sensorLabel: { fontSize: 10, color: "#7A9E7A", fontWeight: "700", letterSpacing: 0.6 },
    sensorValue: { fontSize: 28, fontWeight: "700" },
    sensorUnit: { fontSize: 14, fontWeight: "400", color: "#4A6A4A" },
    sensorRange: { fontSize: 11, color: "#7A9E7A" },
})
