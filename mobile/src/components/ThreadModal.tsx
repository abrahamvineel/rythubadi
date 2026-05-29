/**
 * ThreadModal — slide-up sheet that lets the farmer chat with the advisor about
 * a specific feed event.
 *
 * Layout:
 *   ┌─────────────────────────────┐
 *   │  Header ("Ask Advisor"  ✕)  │  dark green, safe-area-aware
 *   ├─────────────────────────────┤
 *   │  Context card               │  collapsed view of the feed event
 *   ├─────────────────────────────┤
 *   │  Message thread (scrollable)│
 *   ├─────────────────────────────┤
 *   │  Input bar                  │  respects keyboard / home indicator
 *   └─────────────────────────────┘
 */
import React, { useRef, useEffect, useState } from "react"
import {
    Modal,
    View,
    Text,
    ScrollView,
    TextInput,
    TouchableOpacity,
    StyleSheet,
    KeyboardAvoidingView,
    Platform,
    ActivityIndicator,
} from "react-native"
import { useSafeAreaInsets } from "react-native-safe-area-context"
import Markdown from "react-native-markdown-display"
import { FeedEvent, FeedSeverity } from "../types/feed"
import { useThread } from "../hooks/useThread"

const SEVERITY_COLOR: Record<FeedSeverity, string> = {
    info:    "#4CAF50",
    warning: "#FF9800",
    alert:   "#F44336",
}

type Props = {
    visible: boolean
    event: FeedEvent | null
    token: string | null
    language: string
    country: string
    onClose: () => void
}

export function ThreadModal({ visible, event, token, language, country, onClose }: Props) {
    const insets = useSafeAreaInsets()
    const scrollRef = useRef<ScrollView>(null)
    const [text, setText] = useState("")
    const { messages, isLoading, isInitialising, send } = useThread(token, event, language, country)

    // Auto-scroll to bottom as new chunks stream in
    useEffect(() => {
        scrollRef.current?.scrollToEnd({ animated: true })
    }, [messages, isLoading])

    // Clear input when the modal closes
    useEffect(() => {
        if (!visible) setText("")
    }, [visible])

    async function handleSend() {
        const t = text.trim()
        if (!t || isLoading) return
        setText("")
        await send(t)
    }

    if (!event) return null
    const borderColor = SEVERITY_COLOR[event.severity]

    return (
        <Modal
            visible={visible}
            animationType="slide"
            presentationStyle="pageSheet"
            onRequestClose={onClose}
        >
            <KeyboardAvoidingView
                style={{ flex: 1, backgroundColor: "#F4F9F4" }}
                behavior={Platform.OS === "ios" ? "padding" : "height"}
            >
                {/* Modal header */}
                <View style={[styles.modalHeader, { paddingTop: insets.top + 12 }]}>
                    <TouchableOpacity onPress={onClose} style={styles.closeButton} hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}>
                        <Text style={styles.closeText}>✕</Text>
                    </TouchableOpacity>
                    <Text style={styles.modalTitle}>Ask Advisor</Text>
                    {/* Spacer keeps the title visually centred */}
                    <View style={{ width: 36 }} />
                </View>

                {/* Collapsed context card — always visible at the top */}
                <View style={[styles.contextCard, { borderLeftColor: borderColor }]}>
                    <View style={styles.contextRow}>
                        <Text style={styles.contextEmoji}>{event.agent_emoji}</Text>
                        <View style={{ flex: 1 }}>
                            <Text style={styles.contextAgent}>{event.agent}</Text>
                            <Text style={styles.contextTitle} numberOfLines={1}>{event.title}</Text>
                        </View>
                        <View style={[styles.severityDot, { backgroundColor: borderColor }]} />
                    </View>
                    <Text style={styles.contextBody} numberOfLines={2}>{event.body}</Text>
                </View>

                {/* Thread messages */}
                <ScrollView
                    ref={scrollRef}
                    style={{ flex: 1 }}
                    contentContainerStyle={styles.threadContent}
                >
                    {isInitialising && (
                        <View style={styles.centeredRow}>
                            <ActivityIndicator color="#4CAF50" />
                            <Text style={styles.initText}>Loading thread...</Text>
                        </View>
                    )}

                    {!isInitialising && messages.length === 0 && (
                        <View style={styles.emptyThread}>
                            <Text style={styles.emptyEmoji}>💬</Text>
                            <Text style={styles.emptyText}>
                                Ask the advisor about this alert.{"\n"}
                                They'll explain what it means for your farm and what to do next.
                            </Text>
                        </View>
                    )}

                    {messages.map((msg, i) => (
                        <View
                            key={i}
                            style={msg.role === "user" ? styles.userRow : styles.assistantRow}
                        >
                            {msg.role === "assistant" && (
                                <Text style={styles.avatar}>{event.agent_emoji}</Text>
                            )}
                            <View style={msg.role === "user" ? styles.userBubble : styles.assistantBubble}>
                                {msg.role === "user" ? (
                                    <Text style={styles.userText}>{msg.text}</Text>
                                ) : (
                                    <Markdown style={mdStyles}>{msg.text || " "}</Markdown>
                                )}
                            </View>
                        </View>
                    ))}

                    {isLoading && (
                        <View style={styles.assistantRow}>
                            <Text style={styles.avatar}>{event.agent_emoji}</Text>
                            <View style={styles.assistantBubble}>
                                <Text style={styles.typingText}>Thinking...</Text>
                            </View>
                        </View>
                    )}
                </ScrollView>

                {/* Input bar */}
                <View style={[styles.inputBar, { paddingBottom: insets.bottom + 10 }]}>
                    <TextInput
                        style={styles.input}
                        value={text}
                        onChangeText={setText}
                        placeholder="Ask about this alert..."
                        placeholderTextColor="#8FAF8F"
                        multiline
                        maxLength={500}
                        returnKeyType="default"
                    />
                    <TouchableOpacity
                        style={[
                            styles.sendButton,
                            (!text.trim() || isLoading) && styles.sendButtonDisabled,
                        ]}
                        onPress={handleSend}
                        disabled={!text.trim() || isLoading}
                        activeOpacity={0.7}
                    >
                        <Text style={styles.sendLabel}>Send</Text>
                    </TouchableOpacity>
                </View>
            </KeyboardAvoidingView>
        </Modal>
    )
}

const mdStyles = {
    body: { color: "#1A3A1A", fontSize: 14, lineHeight: 21 },
    strong: { fontWeight: "700" as const },
    paragraph: { marginVertical: 2 },
    bullet_list: { marginVertical: 2 },
    code_inline: {
        backgroundColor: "#E8F5E9",
        color: "#1B5E20",
        borderRadius: 4,
        paddingHorizontal: 4,
        fontFamily: "monospace",
    },
}

const styles = StyleSheet.create({
    modalHeader: {
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        paddingHorizontal: 16,
        paddingBottom: 14,
        backgroundColor: "#1B5E20",
    },
    closeButton: {
        width: 36,
        height: 36,
        borderRadius: 18,
        backgroundColor: "rgba(255,255,255,0.15)",
        alignItems: "center",
        justifyContent: "center",
    },
    closeText: { color: "#FFFFFF", fontSize: 16 },
    modalTitle: { color: "#FFFFFF", fontSize: 17, fontWeight: "700" },

    contextCard: {
        borderLeftWidth: 4,
        backgroundColor: "#FFFFFF",
        padding: 14,
        gap: 6,
        borderBottomWidth: 1,
        borderBottomColor: "#D8EDD8",
    },
    contextRow: { flexDirection: "row", alignItems: "center", gap: 8 },
    contextEmoji: { fontSize: 18 },
    contextAgent: { fontSize: 10, color: "#2E7D32", fontWeight: "700", textTransform: "uppercase", letterSpacing: 0.3 },
    contextTitle: { fontSize: 13, fontWeight: "700", color: "#1A3A1A", marginTop: 1 },
    severityDot: { width: 8, height: 8, borderRadius: 4 },
    contextBody: { fontSize: 12, color: "#4A6A4A", lineHeight: 17 },

    threadContent: { padding: 16, gap: 12, paddingBottom: 8 },

    centeredRow: {
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center",
        gap: 10,
        marginTop: 40,
    },
    initText: { color: "#7A9E7A", fontSize: 13 },

    emptyThread: {
        alignItems: "center",
        marginTop: 40,
        gap: 12,
        paddingHorizontal: 24,
    },
    emptyEmoji: { fontSize: 40 },
    emptyText: {
        fontSize: 14,
        color: "#7A9E7A",
        textAlign: "center",
        lineHeight: 21,
    },

    userRow: { flexDirection: "row", justifyContent: "flex-end" },
    assistantRow: { flexDirection: "row", alignItems: "flex-end", gap: 8 },
    avatar: { fontSize: 20, marginBottom: 4 },

    userBubble: {
        backgroundColor: "#2E7D32",
        borderRadius: 16,
        borderBottomRightRadius: 4,
        paddingHorizontal: 14,
        paddingVertical: 9,
        maxWidth: "78%",
    },
    assistantBubble: {
        backgroundColor: "#FFFFFF",
        borderRadius: 16,
        borderBottomLeftRadius: 4,
        paddingHorizontal: 14,
        paddingVertical: 9,
        maxWidth: "78%",
        borderLeftWidth: 3,
        borderLeftColor: "#4CAF50",
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.06,
        shadowRadius: 2,
        elevation: 1,
    },
    userText: { color: "#FFFFFF", fontSize: 14, lineHeight: 20 },
    typingText: { color: "#7A9E7A", fontSize: 14, fontStyle: "italic" },

    inputBar: {
        flexDirection: "row",
        alignItems: "flex-end",
        backgroundColor: "#FFFFFF",
        paddingHorizontal: 12,
        paddingTop: 10,
        gap: 8,
        borderTopWidth: 1,
        borderTopColor: "#D8EDD8",
    },
    input: {
        flex: 1,
        backgroundColor: "#F0F7F0",
        borderRadius: 20,
        paddingHorizontal: 14,
        paddingVertical: 9,
        fontSize: 14,
        color: "#1A3A1A",
        maxHeight: 90,
        borderWidth: 1,
        borderColor: "#C8E6C9",
    },
    sendButton: {
        backgroundColor: "#2E7D32",
        borderRadius: 20,
        paddingHorizontal: 16,
        paddingVertical: 10,
        justifyContent: "center",
    },
    sendButtonDisabled: { backgroundColor: "#A5D6A7" },
    sendLabel: { color: "#FFFFFF", fontWeight: "700", fontSize: 14 },
})
