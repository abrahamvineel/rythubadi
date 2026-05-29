import React, { useState, useEffect } from "react"
import {
    View, Text, TouchableOpacity, StyleSheet, ScrollView,
    ActivityIndicator, Alert,
} from "react-native"
import * as Location from "expo-location"
import { useSafeAreaInsets } from "react-native-safe-area-context"
import { useLocations } from "../hooks/useLocations"
import { PRODUCER_TYPES } from "../constants/producerTypes"
import { API_BASE } from "../constants/api"

type Props = {
    token: string
    onComplete: () => void
}

type CardState = "idle" | "loading" | "done" | "error"

export function OnboardingScreen({ token, onComplete }: Props) {
    const insets = useSafeAreaInsets()
    const { addLocation } = useLocations(token)
    const [producerTypes, setProducerTypes] = useState<string[]>([])
    const [cardState, setCardState] = useState<Record<string, CardState>>({})

    useEffect(() => {
        fetch(`${API_BASE}/profile`, {
            headers: { Authorization: `Bearer ${token}` },
        })
            .then(r => r.json())
            .then(data => setProducerTypes(data.producer_types ?? []))
            .catch(() => {})
    }, [token])

    async function pinLocation(typeValue: string, defaultName: string) {
        setCardState(prev => ({ ...prev, [typeValue]: "loading" }))

        const { status } = await Location.requestForegroundPermissionsAsync()
        if (status !== "granted") {
            Alert.alert(
                "Location permission denied",
                "You can add your farm location later from your profile.",
            )
            setCardState(prev => ({ ...prev, [typeValue]: "idle" }))
            return
        }

        try {
            const pos = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced })
            const result = await addLocation({
                name: defaultName,
                latitude: pos.coords.latitude,
                longitude: pos.coords.longitude,
                producer_types: [typeValue],
            })
            setCardState(prev => ({ ...prev, [typeValue]: result ? "done" : "error" }))
        } catch {
            setCardState(prev => ({ ...prev, [typeValue]: "error" }))
        }
    }

    const typesToShow = PRODUCER_TYPES.filter(pt => producerTypes.includes(pt.value))

    return (
        <ScrollView
            style={styles.root}
            contentContainerStyle={[styles.content, { paddingTop: insets.top + 24, paddingBottom: insets.bottom + 24 }]}
        >
            {/* Header */}
            <View style={styles.header}>
                <Text style={styles.emoji}>📍</Text>
                <Text style={styles.title}>Set up your locations</Text>
                <Text style={styles.subtitle}>
                    Pin where each operation is so Rythu gives you advice based on your exact conditions.
                    You can skip any of these and add them later.
                </Text>
            </View>

            {/* One card per producer type */}
            {typesToShow.length === 0 ? (
                <ActivityIndicator color="#2E7D32" style={{ marginTop: 40 }} />
            ) : (
                typesToShow.map(pt => {
                    const state = cardState[pt.value] ?? "idle"
                    return (
                        <View key={pt.value} style={[styles.card, state === "done" && styles.cardDone]}>
                            <View style={styles.cardHeader}>
                                <Text style={styles.cardEmoji}>{pt.emoji}</Text>
                                <View>
                                    <Text style={styles.cardTitle}>{pt.label} Location</Text>
                                    <Text style={styles.cardHint}>
                                        {state === "done"
                                            ? `✓ "${pt.defaultLocationName}" saved`
                                            : "Where is this operation located?"}
                                    </Text>
                                </View>
                            </View>

                            {state !== "done" && (
                                <TouchableOpacity
                                    style={[styles.gpsButton, state === "loading" && styles.gpsButtonLoading]}
                                    onPress={() => pinLocation(pt.value, pt.defaultLocationName)}
                                    disabled={state === "loading"}
                                >
                                    {state === "loading"
                                        ? <ActivityIndicator color="#fff" size="small" />
                                        : <Text style={styles.gpsButtonText}>📍  Use current GPS</Text>
                                    }
                                </TouchableOpacity>
                            )}

                            {state === "error" && (
                                <Text style={styles.errorText}>Could not get location. Try again or skip.</Text>
                            )}
                        </View>
                    )
                })
            )}

            {/* Continue */}
            <TouchableOpacity style={styles.continueButton} onPress={onComplete}>
                <Text style={styles.continueText}>Continue to Rythu →</Text>
            </TouchableOpacity>

            <Text style={styles.skipNote}>
                You can always add or change locations from your profile.
            </Text>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    root: { flex: 1, backgroundColor: "#F4F9F4" },
    content: { paddingHorizontal: 20, alignItems: "stretch" },

    header: { marginBottom: 28, alignItems: "center" },
    emoji: { fontSize: 44, marginBottom: 12 },
    title: { fontSize: 24, fontWeight: "800", color: "#1B5E20", textAlign: "center", marginBottom: 10 },
    subtitle: { fontSize: 14, color: "#666", textAlign: "center", lineHeight: 20 },

    card: {
        backgroundColor: "#fff", borderRadius: 16, padding: 18,
        marginBottom: 14, borderWidth: 1.5, borderColor: "#E0EDE0",
        shadowColor: "#000", shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.06, shadowRadius: 4, elevation: 2,
    },
    cardDone: { borderColor: "#A5D6A7", backgroundColor: "#F1F8F1" },
    cardHeader: { flexDirection: "row", alignItems: "center", marginBottom: 14 },
    cardEmoji: { fontSize: 32, marginRight: 14 },
    cardTitle: { fontSize: 15, fontWeight: "700", color: "#1B5E20" },
    cardHint: { fontSize: 12, color: "#888", marginTop: 2 },

    gpsButton: {
        backgroundColor: "#2E7D32", borderRadius: 10,
        paddingVertical: 12, alignItems: "center",
    },
    gpsButtonLoading: { backgroundColor: "#A5D6A7" },
    gpsButtonText: { color: "#fff", fontWeight: "700", fontSize: 14 },

    errorText: { color: "#E53935", fontSize: 12, marginTop: 8, textAlign: "center" },

    continueButton: {
        backgroundColor: "#1B5E20", borderRadius: 12,
        paddingVertical: 15, alignItems: "center", marginTop: 12,
    },
    continueText: { color: "#fff", fontSize: 16, fontWeight: "700" },

    skipNote: { textAlign: "center", color: "#9E9E9E", fontSize: 12, marginTop: 14 },
})
