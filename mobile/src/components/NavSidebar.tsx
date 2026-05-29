/**
 * NavSidebar — left-hand navigation for desktop / wide-screen web.
 *
 * Replaces the bottom TabBar when screen width >= 768px.
 * Matches the dark-green brand colour used in all screen headers so the
 * whole app feels like one continuous surface on wide screens.
 */
import React from "react"
import { View, Text, TouchableOpacity, StyleSheet } from "react-native"
import { useSafeAreaInsets } from "react-native-safe-area-context"
import { Tab } from "./TabBar"

type Props = {
    active: Tab
    onSelect: (tab: Tab) => void
    alertCount: number
    onOpenProfile: () => void
    onLogout: () => void
}

const NAV_ITEMS: { id: Tab; label: string; emoji: string }[] = [
    { id: "feed",    label: "Farm Feed",  emoji: "🔔" },
    { id: "monitor", label: "Monitor",    emoji: "📡" },
    { id: "chats",   label: "Chats",      emoji: "💬" },
]

export function NavSidebar({ active, onSelect, alertCount, onOpenProfile, onLogout }: Props) {
    const insets = useSafeAreaInsets()

    return (
        <View style={[
            styles.sidebar,
            { paddingTop: insets.top + 20, paddingBottom: insets.bottom + 16 },
        ]}>
            {/* Brand */}
            <View style={styles.brand}>
                <Text style={styles.brandEmoji}>🌾</Text>
                <View>
                    <Text style={styles.brandName}>Rythu</Text>
                    <Text style={styles.brandSub}>AI farm advisor</Text>
                </View>
            </View>

            <View style={styles.divider} />

            {/* Navigation items */}
            <View style={styles.navSection}>
                {NAV_ITEMS.map(item => {
                    const isActive = item.id === active
                    const showBadge = item.id === "feed" && alertCount > 0
                    return (
                        <TouchableOpacity
                            key={item.id}
                            style={[styles.navItem, isActive && styles.navItemActive]}
                            onPress={() => onSelect(item.id)}
                            activeOpacity={0.7}
                        >
                            {isActive && <View style={styles.activeAccent} />}
                            <View style={styles.navIconWrap}>
                                <Text style={[styles.navEmoji, isActive && styles.navEmojiActive]}>
                                    {item.emoji}
                                </Text>
                                {showBadge && (
                                    <View style={styles.badge}>
                                        <Text style={styles.badgeText}>
                                            {alertCount > 9 ? "9+" : String(alertCount)}
                                        </Text>
                                    </View>
                                )}
                            </View>
                            <Text style={[styles.navLabel, isActive && styles.navLabelActive]}>
                                {item.label}
                            </Text>
                        </TouchableOpacity>
                    )
                })}
            </View>

            {/* Spacer pushes profile + logout to the bottom */}
            <View style={{ flex: 1 }} />

            <View style={styles.divider} />

            {/* Profile */}
            <TouchableOpacity
                style={styles.bottomItem}
                onPress={onOpenProfile}
                activeOpacity={0.7}
            >
                <View style={styles.profileAvatar}>
                    <Text style={{ fontSize: 15 }}>👤</Text>
                </View>
                <Text style={styles.bottomLabel}>Profile</Text>
            </TouchableOpacity>

            {/* Logout */}
            <TouchableOpacity
                style={[styles.bottomItem, styles.logoutItem]}
                onPress={onLogout}
                activeOpacity={0.7}
            >
                <Text style={styles.logoutEmoji}>⏻</Text>
                <Text style={styles.logoutLabel}>Log out</Text>
            </TouchableOpacity>
        </View>
    )
}

const styles = StyleSheet.create({
    sidebar: {
        width: 220,
        backgroundColor: "#1B5E20",
        flexDirection: "column",
        paddingHorizontal: 12,
        // Subtle right border separates sidebar from content
        borderRightWidth: 1,
        borderRightColor: "#2E7D32",
    },

    brand: {
        flexDirection: "row",
        alignItems: "center",
        gap: 10,
        paddingHorizontal: 8,
        paddingBottom: 4,
    },
    brandEmoji: { fontSize: 28 },
    brandName: { fontSize: 18, fontWeight: "700", color: "#FFFFFF", letterSpacing: 0.5 },
    brandSub: { fontSize: 10, color: "#81C784", marginTop: 1 },

    divider: { height: 1, backgroundColor: "#2E7D32", marginVertical: 12 },

    navSection: { gap: 2 },

    navItem: {
        flexDirection: "row",
        alignItems: "center",
        gap: 10,
        paddingVertical: 11,
        paddingHorizontal: 10,
        borderRadius: 10,
        position: "relative",
    },
    navItemActive: {
        backgroundColor: "#2E7D32",
    },
    // Green left accent bar on the active item
    activeAccent: {
        position: "absolute",
        left: 0,
        top: 8,
        bottom: 8,
        width: 3,
        backgroundColor: "#A5D6A7",
        borderRadius: 2,
    },
    navIconWrap: {
        position: "relative",
        width: 26,
        alignItems: "center",
    },
    navEmoji: { fontSize: 18, opacity: 0.6 },
    navEmojiActive: { opacity: 1 },
    navLabel: { fontSize: 14, color: "#A5D6A7", fontWeight: "500" },
    navLabelActive: { color: "#FFFFFF", fontWeight: "700" },

    badge: {
        position: "absolute",
        top: -5,
        right: -8,
        backgroundColor: "#F44336",
        borderRadius: 8,
        minWidth: 16,
        height: 16,
        alignItems: "center",
        justifyContent: "center",
        paddingHorizontal: 3,
    },
    badgeText: { color: "#FFFFFF", fontSize: 9, fontWeight: "700" },

    bottomItem: {
        flexDirection: "row",
        alignItems: "center",
        gap: 10,
        paddingVertical: 10,
        paddingHorizontal: 10,
        borderRadius: 10,
    },
    profileAvatar: {
        width: 30,
        height: 30,
        borderRadius: 15,
        backgroundColor: "#2E7D32",
        alignItems: "center",
        justifyContent: "center",
    },
    bottomLabel: { fontSize: 14, color: "#A5D6A7", fontWeight: "500" },

    logoutItem: { marginTop: 2 },
    logoutEmoji: { fontSize: 18, color: "#EF9A9A", width: 30, textAlign: "center" },
    logoutLabel: { fontSize: 14, color: "#EF9A9A", fontWeight: "500" },
})
