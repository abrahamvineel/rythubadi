import React from "react"
import { View, Text, TouchableOpacity, StyleSheet } from "react-native"
import { FeedEvent, FeedSeverity } from "../types/feed"

type Props = {
    event: FeedEvent
    onReply: (event: FeedEvent) => void
    // Called when the farmer taps "View <subject_name>".
    // The parent decides where to navigate based on subject_type.
    onViewSubject?: (event: FeedEvent) => void
}

const SEVERITY_BORDER: Record<FeedSeverity, string> = {
    info:    "#4CAF50",
    warning: "#FF9800",
    alert:   "#F44336",
}

const SEVERITY_BG: Record<FeedSeverity, string> = {
    info:    "#F1FFF1",
    warning: "#FFF8EE",
    alert:   "#FFF3F3",
}

const SEVERITY_LABEL: Record<FeedSeverity, string> = {
    info:    "Info",
    warning: "Warning",
    alert:   "Alert",
}

function timeAgo(iso: string): string {
    const diff = Date.now() - new Date(iso).getTime()
    const mins = Math.floor(diff / 60_000)
    if (mins < 1) return "just now"
    if (mins < 60) return `${mins}m ago`
    const hrs = Math.floor(mins / 60)
    if (hrs < 24) return `${hrs}h ago`
    return `${Math.floor(hrs / 24)}d ago`
}

export function FeedCard({ event, onReply, onViewSubject }: Props) {
    const borderColor = SEVERITY_BORDER[event.severity]
    const bgColor = SEVERITY_BG[event.severity]
    const hasSubject = !!event.subject_id

    return (
        <View style={[styles.card, { borderLeftColor: borderColor, backgroundColor: bgColor }]}>
            {/* Header: agent + severity pill + timestamp */}
            <View style={styles.header}>
                <Text style={styles.agentEmoji}>{event.agent_emoji}</Text>
                <View style={{ flex: 1 }}>
                    <Text style={styles.agentName}>{event.agent}</Text>
                    <Text style={styles.timestamp}>{timeAgo(event.created_at)}</Text>
                </View>
                <View style={[styles.severityPill, { backgroundColor: borderColor }]}>
                    <Text style={styles.severityText}>{SEVERITY_LABEL[event.severity]}</Text>
                </View>
            </View>

            {/* Subject label — shown when the event is about a named entity */}
            {hasSubject && (
                <View style={[styles.subjectTag, { borderColor: borderColor + "55", backgroundColor: borderColor + "11" }]}>
                    <Text style={[styles.subjectText, { color: borderColor }]}>
                        {event.subject_name}
                    </Text>
                </View>
            )}

            {/* Content */}
            <Text style={styles.title}>{event.title}</Text>
            <Text style={styles.body} numberOfLines={3}>{event.body}</Text>

            {/* Action row */}
            <View style={styles.actions}>
                {/* Reply always takes flex: 1 */}
                <TouchableOpacity
                    style={[styles.replyButton, !hasSubject && styles.replyButtonFull]}
                    onPress={() => onReply(event)}
                    activeOpacity={0.7}
                >
                    <Text style={styles.replyButtonText}>
                        {event.reply_count > 0
                            ? `💬 ${event.reply_count} repl${event.reply_count === 1 ? "y" : "ies"}`
                            : "💬 Ask advisor"}
                    </Text>
                </TouchableOpacity>

                {/* "View <subject_name>" — only shown when event links to a navigable entity */}
                {hasSubject && onViewSubject && (
                    <TouchableOpacity
                        style={[styles.viewButton, { backgroundColor: borderColor }]}
                        onPress={() => onViewSubject(event)}
                        activeOpacity={0.8}
                    >
                        <Text style={styles.viewButtonText} numberOfLines={1}>
                            View {event.subject_name}
                        </Text>
                    </TouchableOpacity>
                )}
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    card: {
        borderLeftWidth: 4,
        borderRadius: 14,
        padding: 14,
        gap: 8,
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.06,
        shadowRadius: 3,
        elevation: 2,
    },
    header: {
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
    },
    agentEmoji: { fontSize: 20 },
    agentName: {
        fontSize: 11,
        fontWeight: "700",
        color: "#2E7D32",
        textTransform: "uppercase",
        letterSpacing: 0.3,
    },
    timestamp: {
        fontSize: 10,
        color: "#7A9E7A",
        marginTop: 1,
    },
    severityPill: {
        borderRadius: 10,
        paddingHorizontal: 8,
        paddingVertical: 3,
    },
    severityText: {
        color: "#FFFFFF",
        fontSize: 9,
        fontWeight: "700",
        textTransform: "uppercase",
        letterSpacing: 0.6,
    },

    // Subject tag — small chip showing which entity this is about
    subjectTag: {
        alignSelf: "flex-start",
        borderRadius: 6,
        borderWidth: 1,
        paddingHorizontal: 8,
        paddingVertical: 3,
    },
    subjectText: {
        fontSize: 11,
        fontWeight: "600",
    },

    title: {
        fontSize: 14,
        fontWeight: "700",
        color: "#1A3A1A",
        lineHeight: 20,
    },
    body: {
        fontSize: 13,
        color: "#4A6A4A",
        lineHeight: 19,
    },

    actions: {
        flexDirection: "row",
        alignItems: "center",
        gap: 8,
        marginTop: 2,
    },
    replyButton: {
        flex: 1,
        backgroundColor: "#FFFFFF",
        borderRadius: 8,
        paddingVertical: 8,
        paddingHorizontal: 12,
        borderWidth: 1,
        borderColor: "#C8E6C9",
        alignItems: "center",
    },
    // When there's no view button, reply button spans full width — already handled by flex:1
    replyButtonFull: {},
    replyButtonText: {
        fontSize: 12,
        fontWeight: "700",
        color: "#2E7D32",
    },
    viewButton: {
        borderRadius: 8,
        paddingVertical: 8,
        paddingHorizontal: 12,
        alignItems: "center",
        minWidth: 90,
        maxWidth: 190,
    },
    viewButtonText: {
        fontSize: 12,
        fontWeight: "700",
        color: "#FFFFFF",
    },
})
