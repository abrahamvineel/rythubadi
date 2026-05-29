import React, { useState, useEffect } from "react"
import {
    Modal, View, Text, TouchableOpacity, StyleSheet,
    ActivityIndicator, Pressable, ScrollView, Alert,
} from "react-native"
import * as Location from "expo-location"
import { API_BASE } from "../constants/api"
import { PRODUCER_TYPES } from "../constants/producerTypes"
import { useLocations } from "../hooks/useLocations"
import { getFarmLocation } from "../utils/location"

type LocCardState = "idle" | "loading" | "done" | "error"

type Props = {
    visible: boolean
    token: string | null
    onClose: () => void
    onLogout?: () => void
}

export function ProfileSheet({ visible, token, onClose, onLogout }: Props) {
    // ── Producer types ────────────────────────────────────────────────────────
    const [currentTypes, setCurrentTypes] = useState<string[]>([])
    const [pendingAdd, setPendingAdd] = useState<string[]>([])
    const [loadingTypes, setLoadingTypes] = useState(false)
    const [saving, setSaving] = useState(false)
    const [saved, setSaved] = useState(false)

    // ── Locations ─────────────────────────────────────────────────────────────
    const { locations, loaded: locLoaded, addLocation, removeLocation, reload: reloadLocations } = useLocations(token)
    const [locCardState, setLocCardState] = useState<Record<string, LocCardState>>({})

    // Load current producer types when sheet opens
    useEffect(() => {
        if (!visible || !token) return
        setLoadingTypes(true)
        setPendingAdd([])
        setSaved(false)
        setLocCardState({})
        fetch(`${API_BASE}/profile`, {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then(r => r.json())
            .then(data => setCurrentTypes(data.producer_types ?? []))
            .catch(() => {})
            .finally(() => setLoadingTypes(false))
        reloadLocations()
    }, [visible, token])

    // ── Producer type handlers ─────────────────────────────────────────────────
    function togglePending(value: string) {
        if (currentTypes.includes(value)) return   // add-only: can't deselect current
        setPendingAdd(prev =>
            prev.includes(value) ? prev.filter(t => t !== value) : [...prev, value]
        )
    }

    async function handleSave() {
        if (pendingAdd.length === 0) { onClose(); return }
        setSaving(true)
        try {
            const res = await fetch(`${API_BASE}/profile/types`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
                body: JSON.stringify({ producer_types: pendingAdd }),
            })
            const data = await res.json()
            setCurrentTypes(data.producer_types ?? [])
            setPendingAdd([])
            setSaved(true)
        } catch {}
        setSaving(false)
    }

    // ── Location handlers ──────────────────────────────────────────────────────
    async function handleAddLocation(typeValue: string, defaultName: string) {
        setLocCardState(prev => ({ ...prev, [typeValue]: "loading" }))
        const { status } = await Location.requestForegroundPermissionsAsync()
        if (status !== "granted") {
            Alert.alert(
                "Location permission denied",
                "Grant location permission in your device settings to pin a farm location.",
            )
            setLocCardState(prev => ({ ...prev, [typeValue]: "idle" }))
            return
        }
        try {
            const pos = await getFarmLocation()
            const result = await addLocation({
                name: defaultName,
                latitude: pos.coords.latitude,
                longitude: pos.coords.longitude,
                producer_types: [typeValue],
            })
            setLocCardState(prev => ({ ...prev, [typeValue]: result ? "done" : "error" }))
        } catch {
            setLocCardState(prev => ({ ...prev, [typeValue]: "error" }))
        }
    }

    async function handleDeleteLocation(id: string) {
        Alert.alert(
            "Remove location?",
            "This farm location will be removed from your profile.",
            [
                { text: "Cancel", style: "cancel" },
                {
                    text: "Remove",
                    style: "destructive",
                    onPress: async () => { await removeLocation(id) },
                },
            ],
        )
    }

    const allSelected = [...currentTypes, ...pendingAdd]

    return (
        <Modal visible={visible} transparent animationType="slide" onRequestClose={onClose}>
            <Pressable style={styles.overlay} onPress={onClose} />
            <View style={styles.sheet}>
                {/* Handle bar */}
                <View style={styles.handle} />

                <ScrollView showsVerticalScrollIndicator={false} bounces={false}>
                    {/* ── Producer types section ── */}
                    <Text style={styles.title}>What do you produce?</Text>
                    <Text style={styles.subtitle}>
                        {saved ? "✓ Types updated!" : "Tap a new type to add it to your profile"}
                    </Text>

                    {loadingTypes ? (
                        <ActivityIndicator color="#2E7D32" style={{ marginVertical: 32 }} />
                    ) : (
                        <View style={styles.typeGrid}>
                            {PRODUCER_TYPES.map(pt => {
                                const isActive = currentTypes.includes(pt.value)
                                const isPending = pendingAdd.includes(pt.value)
                                const isSelected = isActive || isPending
                                return (
                                    <TouchableOpacity
                                        key={pt.value}
                                        style={[
                                            styles.typeCard,
                                            isSelected && styles.typeCardSelected,
                                            isActive && styles.typeCardLocked,
                                        ]}
                                        onPress={() => togglePending(pt.value)}
                                        activeOpacity={isActive ? 1 : 0.75}
                                    >
                                        <Text style={styles.typeEmoji}>{pt.emoji}</Text>
                                        <Text style={[styles.typeLabel, isSelected && styles.typeLabelSelected]}>
                                            {pt.label}
                                        </Text>
                                        {isActive && <Text style={styles.badge}>current</Text>}
                                        {isPending && <Text style={styles.badgePending}>+ add</Text>}
                                    </TouchableOpacity>
                                )
                            })}
                        </View>
                    )}

                    <TouchableOpacity
                        style={[styles.saveButton, (saving || pendingAdd.length === 0) && styles.saveButtonMuted]}
                        onPress={handleSave}
                        disabled={saving}
                    >
                        {saving
                            ? <ActivityIndicator color="#fff" />
                            : <Text style={styles.saveButtonText}>
                                {pendingAdd.length > 0 ? `Add ${pendingAdd.length} type${pendingAdd.length > 1 ? "s" : ""}` : "Done"}
                              </Text>
                        }
                    </TouchableOpacity>

                    {/* ── Locations section ── */}
                    <View style={styles.divider} />

                    <Text style={styles.title}>📍 Your Farm Locations</Text>
                    <Text style={styles.subtitle}>Locations give Rythu field-level weather accuracy</Text>

                    {!locLoaded ? (
                        <ActivityIndicator color="#2E7D32" style={{ marginVertical: 16 }} />
                    ) : (
                        <>
                            {/* Existing locations */}
                            {locations.length > 0 ? (
                                locations.map(loc => (
                                    <View key={loc.id} style={styles.locRow}>
                                        <Text style={styles.locEmoji}>📍</Text>
                                        <View style={{ flex: 1 }}>
                                            <Text style={styles.locName}>{loc.name}</Text>
                                            <Text style={styles.locTypes}>
                                                {loc.producer_types
                                                    .map(t => PRODUCER_TYPES.find(p => p.value === t)?.label ?? t)
                                                    .join(" · ")}
                                            </Text>
                                        </View>
                                        <TouchableOpacity
                                            onPress={() => handleDeleteLocation(loc.id)}
                                            style={styles.locDeleteBtn}
                                            hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
                                        >
                                            <Text style={styles.locDeleteIcon}>🗑</Text>
                                        </TouchableOpacity>
                                    </View>
                                ))
                            ) : (
                                <Text style={styles.emptyNote}>No locations pinned yet</Text>
                            )}

                            {/* Add location per type */}
                            {currentTypes.length > 0 && (
                                <View style={{ marginTop: 12 }}>
                                    <Text style={styles.addLocHeading}>Pin a location for each operation</Text>
                                    {currentTypes.map(typeValue => {
                                        const pt = PRODUCER_TYPES.find(p => p.value === typeValue)
                                        if (!pt) return null
                                        const state = locCardState[typeValue] ?? "idle"
                                        return (
                                            <TouchableOpacity
                                                key={typeValue}
                                                style={[
                                                    styles.addLocButton,
                                                    state === "loading" && styles.addLocButtonLoading,
                                                    state === "done" && styles.addLocButtonDone,
                                                ]}
                                                onPress={() => handleAddLocation(typeValue, pt.defaultLocationName)}
                                                disabled={state === "loading" || state === "done"}
                                                activeOpacity={0.75}
                                            >
                                                {state === "loading" ? (
                                                    <ActivityIndicator color="#fff" size="small" />
                                                ) : (
                                                    <Text style={styles.addLocText}>
                                                        {state === "done"
                                                            ? `✓ ${pt.defaultLocationName} saved`
                                                            : `📍  Use GPS for ${pt.label}`}
                                                    </Text>
                                                )}
                                                {state === "error" && (
                                                    <Text style={styles.addLocError}>Could not get location</Text>
                                                )}
                                            </TouchableOpacity>
                                        )
                                    })}
                                </View>
                            )}
                        </>
                    )}

                    {/* ── Logout section ── */}
                    {onLogout && (
                        <>
                            <View style={styles.divider} />
                            <TouchableOpacity
                                style={styles.logoutButton}
                                onPress={() => {
                                    Alert.alert(
                                        "Log out?",
                                        "You'll need to sign in again to access your farm data.",
                                        [
                                            { text: "Cancel", style: "cancel" },
                                            { text: "Log out", style: "destructive", onPress: () => { onClose(); onLogout() } },
                                        ],
                                    )
                                }}
                                activeOpacity={0.8}
                            >
                                <Text style={styles.logoutText}>⏻  Log out</Text>
                            </TouchableOpacity>
                        </>
                    )}

                    {/* Bottom spacer so last item isn't flush with edge */}
                    <View style={{ height: 16 }} />
                </ScrollView>
            </View>
        </Modal>
    )
}

const styles = StyleSheet.create({
    overlay: { flex: 1, backgroundColor: "rgba(0,0,0,0.45)" },
    sheet: {
        backgroundColor: "#fff",
        borderTopLeftRadius: 24,
        borderTopRightRadius: 24,
        paddingTop: 16,
        paddingHorizontal: 24,
        paddingBottom: 36,
        maxHeight: "85%",
    },
    handle: {
        width: 40, height: 4, backgroundColor: "#D8EDD8",
        borderRadius: 2, alignSelf: "center", marginBottom: 20,
    },
    title: { fontSize: 18, fontWeight: "700", color: "#1B5E20", marginBottom: 4 },
    subtitle: { fontSize: 13, color: "#888", marginBottom: 20 },

    // Producer type grid
    typeGrid: { flexDirection: "row", flexWrap: "wrap", gap: 10, marginBottom: 24 },
    typeCard: {
        width: "47%", borderRadius: 14, borderWidth: 1.5,
        borderColor: "#D8EDD8", backgroundColor: "#F8FBF8",
        padding: 14, alignItems: "center", minHeight: 86,
        justifyContent: "center", position: "relative",
    },
    typeCardSelected: { borderColor: "#2E7D32", backgroundColor: "#E8F5E9" },
    typeCardLocked: { borderColor: "#A5D6A7", backgroundColor: "#F1F8F1" },
    typeEmoji: { fontSize: 26, marginBottom: 6 },
    typeLabel: { fontSize: 13, fontWeight: "600", color: "#555", textAlign: "center" },
    typeLabelSelected: { color: "#1B5E20" },
    badge: {
        position: "absolute", top: 7, right: 8,
        fontSize: 9, fontWeight: "700", color: "#2E7D32",
        backgroundColor: "#C8E6C9", paddingHorizontal: 5, paddingVertical: 2,
        borderRadius: 6, overflow: "hidden",
    },
    badgePending: {
        position: "absolute", top: 7, right: 8,
        fontSize: 9, fontWeight: "700", color: "#fff",
        backgroundColor: "#2E7D32", paddingHorizontal: 5, paddingVertical: 2,
        borderRadius: 6, overflow: "hidden",
    },

    saveButton: {
        backgroundColor: "#2E7D32", borderRadius: 12,
        paddingVertical: 14, alignItems: "center",
    },
    saveButtonMuted: { backgroundColor: "#A5D6A7" },
    saveButtonText: { color: "#fff", fontSize: 15, fontWeight: "700" },

    divider: { height: 1, backgroundColor: "#E8F5E9", marginVertical: 24 },

    // Existing location rows
    locRow: {
        flexDirection: "row", alignItems: "center",
        backgroundColor: "#F8FBF8", borderRadius: 12,
        borderWidth: 1.5, borderColor: "#E0EDE0",
        paddingHorizontal: 14, paddingVertical: 12,
        marginBottom: 10,
    },
    locEmoji: { fontSize: 20, marginRight: 12 },
    locName: { fontSize: 14, fontWeight: "700", color: "#1A3A1A" },
    locTypes: { fontSize: 12, color: "#888", marginTop: 2 },
    locDeleteBtn: { padding: 4 },
    locDeleteIcon: { fontSize: 17 },
    emptyNote: { fontSize: 13, color: "#aaa", textAlign: "center", marginVertical: 12 },

    // Add location buttons
    addLocHeading: { fontSize: 13, fontWeight: "600", color: "#555", marginBottom: 10 },
    addLocButton: {
        backgroundColor: "#2E7D32", borderRadius: 10,
        paddingVertical: 12, paddingHorizontal: 16,
        alignItems: "center", marginBottom: 10,
    },
    addLocButtonLoading: { backgroundColor: "#A5D6A7" },
    addLocButtonDone: { backgroundColor: "#4CAF50" },
    addLocText: { color: "#fff", fontWeight: "700", fontSize: 14 },
    addLocError: { color: "#ffcdd2", fontSize: 12, marginTop: 4 },

    logoutButton: {
        borderRadius: 12,
        paddingVertical: 14,
        alignItems: "center",
        borderWidth: 1.5,
        borderColor: "#FFCDD2",
        backgroundColor: "#FFF5F5",
    },
    logoutText: { color: "#C62828", fontSize: 15, fontWeight: "700" },
})
