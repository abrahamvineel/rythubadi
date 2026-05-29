import React, { useState, useCallback } from "react"
import {
    View,
    Text,
    ScrollView,
    StyleSheet,
    TouchableOpacity,
    ActivityIndicator,
    RefreshControl,
    useWindowDimensions,
} from "react-native"
import { useSafeAreaInsets } from "react-native-safe-area-context"

const DESKTOP_BREAKPOINT = 768
import { useFeed } from "../hooks/useFeed"
import { FeedCard } from "../components/FeedCard"
import { ThreadModal } from "../components/ThreadModal"
import { FeedEvent } from "../types/feed"

type Props = {
    token: string | null
    language: string
    country: string
    onOpenProfile: () => void
    // Propagated from App.tsx — parent handles the tab switch + Monitor navigation
    onViewSubject?: (event: FeedEvent) => void
}

function groupByDate(events: FeedEvent[]): { date: string; items: FeedEvent[] }[] {
    const groups: Record<string, FeedEvent[]> = {}
    const today = new Date()
    const yesterday = new Date()
    yesterday.setDate(today.getDate() - 1)

    for (const e of events) {
        const d = new Date(e.created_at)
        let label: string
        if (d.toDateString() === today.toDateString()) label = "Today"
        else if (d.toDateString() === yesterday.toDateString()) label = "Yesterday"
        else label = d.toLocaleDateString("en-US", { month: "short", day: "numeric" })
        if (!groups[label]) groups[label] = []
        groups[label].push(e)
    }

    return Object.entries(groups).map(([date, items]) => ({ date, items }))
}

export function FeedScreen({ token, language, country, onOpenProfile, onViewSubject }: Props) {
    const insets = useSafeAreaInsets()
    const { width } = useWindowDimensions()
    const isDesktop = width >= DESKTOP_BREAKPOINT
    const { events, loading, unreadAlerts, reload } = useFeed(token)
    const [threadEvent, setThreadEvent] = useState<FeedEvent | null>(null)
    const [refreshing, setRefreshing] = useState(false)

    const handleRefresh = useCallback(async () => {
        setRefreshing(true)
        await reload()
        setRefreshing(false)
    }, [reload])

    const groups = groupByDate(events)
    const alertEvents = events.filter(e => e.severity === "alert")

    return (
        <View style={[styles.root, { paddingTop: insets.top }]}>
            {/* Screen header — on desktop the sidebar provides navigation context,
                so we use a lighter inline title instead of the full dark bar */}
            <View style={[styles.header, isDesktop && styles.headerDesktop]}>
                <View style={{ flex: 1 }}>
                    <Text style={[styles.headerTitle, isDesktop && styles.headerTitleDesktop]}>
                        Farm Feed
                    </Text>
                    <Text style={[styles.headerSub, isDesktop && styles.headerSubDesktop]}>
                        {events.length > 0
                            ? `${events.length} update${events.length !== 1 ? "s" : ""} from your agents`
                            : "Your agents are watching"}
                    </Text>
                </View>
                {/* Profile avatar — only shown on mobile; sidebar has Profile on desktop */}
                {!isDesktop && (
                    <TouchableOpacity onPress={onOpenProfile} style={styles.avatarBtn} activeOpacity={0.7}>
                        <Text style={{ fontSize: 18 }}>👤</Text>
                    </TouchableOpacity>
                )}
            </View>

            {/* Critical alert banner — tapping opens the first alert's thread */}
            {alertEvents.length > 0 && (
                <TouchableOpacity
                    style={styles.alertBanner}
                    onPress={() => setThreadEvent(alertEvents[0])}
                    activeOpacity={0.85}
                >
                    <Text style={styles.alertBannerText}>
                        🚨  {alertEvents.length} active alert{alertEvents.length > 1 ? "s" : ""} — tap to review
                    </Text>
                </TouchableOpacity>
            )}

            {loading && events.length === 0 ? (
                <View style={styles.loadingCenter}>
                    <ActivityIndicator color="#4CAF50" size="large" />
                    <Text style={styles.loadingText}>Loading your farm feed...</Text>
                </View>
            ) : (
                <ScrollView
                    style={{ flex: 1 }}
                    contentContainerStyle={styles.listContent}
                    showsVerticalScrollIndicator={false}
                    refreshControl={
                        <RefreshControl
                            refreshing={refreshing}
                            onRefresh={handleRefresh}
                            tintColor="#4CAF50"
                        />
                    }
                >
                    {events.length === 0 && (
                        <View style={styles.emptyState}>
                            <Text style={styles.emptyEmoji}>🌱</Text>
                            <Text style={styles.emptyTitle}>All quiet on the farm</Text>
                            <Text style={styles.emptySub}>
                                Your agents are monitoring your crops and livestock.{"\n"}
                                Updates will appear here as they happen.
                            </Text>
                        </View>
                    )}

                    {groups.map(({ date, items }) => (
                        <View key={date} style={styles.dateGroup}>
                            <View style={styles.dateDivider}>
                                <View style={styles.dividerLine} />
                                <Text style={styles.dividerLabel}>{date}</Text>
                                <View style={styles.dividerLine} />
                            </View>
                            {items.map(event => (
                                <FeedCard
                                    key={event.id}
                                    event={event}
                                    onReply={setThreadEvent}
                                    onViewSubject={onViewSubject}
                                />
                            ))}
                        </View>
                    ))}
                </ScrollView>
            )}

            <ThreadModal
                visible={threadEvent !== null}
                event={threadEvent}
                token={token}
                language={language}
                country={country}
                onClose={() => setThreadEvent(null)}
            />
        </View>
    )
}

const styles = StyleSheet.create({
    root: { flex: 1, backgroundColor: "#F4F9F4" },

    header: {
        flexDirection: "row",
        alignItems: "center",
        paddingHorizontal: 20,
        paddingVertical: 14,
        backgroundColor: "#1B5E20",
    },
    // Desktop: no dark bar — sidebar already gives context. Light background, dark text.
    headerDesktop: {
        backgroundColor: "#F4F9F4",
        paddingVertical: 16,
        borderBottomWidth: 1,
        borderBottomColor: "#D8EDD8",
    },
    headerTitle: { fontSize: 20, fontWeight: "700", color: "#FFFFFF" },
    headerTitleDesktop: { fontSize: 22, color: "#1B5E20" },
    headerSub: { fontSize: 12, color: "#A5D6A7", marginTop: 2 },
    headerSubDesktop: { color: "#7A9E7A" },
    avatarBtn: {
        width: 36, height: 36, borderRadius: 18,
        backgroundColor: "rgba(255,255,255,0.15)",
        alignItems: "center", justifyContent: "center",
    },

    alertBanner: {
        backgroundColor: "#C62828",
        paddingVertical: 10,
        paddingHorizontal: 20,
    },
    alertBannerText: { color: "#FFFFFF", fontWeight: "700", fontSize: 13, textAlign: "center" },

    loadingCenter: { flex: 1, alignItems: "center", justifyContent: "center", gap: 12 },
    loadingText: { color: "#7A9E7A", fontSize: 14 },

    listContent: { padding: 16, paddingBottom: 24 },
    dateGroup: { gap: 10, marginBottom: 6 },

    dateDivider: {
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
        marginBottom: 4,
        marginTop: 8,
    },
    dividerLine: { flex: 1, height: 1, backgroundColor: "#C8E6C9" },
    dividerLabel: {
        fontSize: 10, color: "#7A9E7A", fontWeight: "700",
        textTransform: "uppercase", letterSpacing: 0.8,
    },

    emptyState: { alignItems: "center", marginTop: 60, gap: 12 },
    emptyEmoji: { fontSize: 52 },
    emptyTitle: { fontSize: 18, fontWeight: "700", color: "#2E7D32" },
    emptySub: { fontSize: 14, color: "#7A9E7A", textAlign: "center", lineHeight: 21 },
})
