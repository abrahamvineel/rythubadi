import React from "react"
import { View, Text, TouchableOpacity, StyleSheet } from "react-native"
import { useSafeAreaInsets } from "react-native-safe-area-context"

export type Tab = "feed" | "monitor" | "chats"

type Props = {
    active: Tab
    onSelect: (tab: Tab) => void
    alertCount: number
}

const TABS: { id: Tab; label: string; emoji: string }[] = [
    { id: "feed",    label: "Feed",    emoji: "🔔" },
    { id: "monitor", label: "Monitor", emoji: "📡" },
    { id: "chats",   label: "Chats",   emoji: "💬" },
]

export function TabBar({ active, onSelect, alertCount }: Props) {
    const insets = useSafeAreaInsets()

    return (
        <View style={[styles.bar, { paddingBottom: insets.bottom + 4 }]}>
            {TABS.map(tab => {
                const isActive = tab.id === active
                // Red alert badge appears on the Feed tab (not Monitor) — alerts live in the feed
                const showBadge = tab.id === "feed" && alertCount > 0
                return (
                    <TouchableOpacity
                        key={tab.id}
                        style={styles.tab}
                        onPress={() => onSelect(tab.id)}
                        activeOpacity={0.7}
                    >
                        {isActive && <View style={styles.activeBar} />}
                        <View style={styles.iconWrap}>
                            <Text style={[styles.emoji, isActive && styles.emojiActive]}>
                                {tab.emoji}
                            </Text>
                            {showBadge && (
                                <View style={styles.badge}>
                                    <Text style={styles.badgeText}>
                                        {alertCount > 9 ? "9+" : String(alertCount)}
                                    </Text>
                                </View>
                            )}
                        </View>
                        <Text style={[styles.label, isActive && styles.labelActive]}>
                            {tab.label}
                        </Text>
                    </TouchableOpacity>
                )
            })}
        </View>
    )
}

const styles = StyleSheet.create({
    bar: {
        flexDirection: "row",
        backgroundColor: "#FFFFFF",
        borderTopWidth: 1,
        borderTopColor: "#D8EDD8",
        paddingTop: 8,
    },
    tab: {
        flex: 1,
        alignItems: "center",
        gap: 2,
        position: "relative",
        paddingTop: 4,
    },
    activeBar: {
        position: "absolute",
        top: 0,
        left: "20%",
        right: "20%",
        height: 3,
        backgroundColor: "#2E7D32",
        borderRadius: 2,
    },
    iconWrap: {
        position: "relative",
    },
    emoji: {
        fontSize: 22,
        opacity: 0.45,
    },
    emojiActive: {
        opacity: 1,
    },
    label: {
        fontSize: 10,
        color: "#7A9E7A",
        fontWeight: "500",
    },
    labelActive: {
        color: "#1B5E20",
        fontWeight: "700",
    },
    badge: {
        position: "absolute",
        top: -4,
        right: -10,
        backgroundColor: "#F44336",
        borderRadius: 8,
        minWidth: 16,
        height: 16,
        alignItems: "center",
        justifyContent: "center",
        paddingHorizontal: 3,
    },
    badgeText: {
        color: "#FFFFFF",
        fontSize: 9,
        fontWeight: "700",
    },
})
