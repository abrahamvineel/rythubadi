/**
 * ChatsScreen — master-detail chat interface.
 *
 * List view:  all conversations, "New Chat" button, delete button per row.
 * Detail view: message thread + streaming, image picker, voice button.
 *
 * The two views share a single component so the TabBar stays visible in both.
 * Back button in the detail header returns to the list.
 */
import React, { useState, useRef, useEffect } from "react"
import {
    View,
    Text,
    ScrollView,
    TextInput,
    StyleSheet,
    TouchableOpacity,
    Pressable,
    Image,
    KeyboardAvoidingView,
    Platform,
    useWindowDimensions,
} from "react-native"
import { useSafeAreaInsets } from "react-native-safe-area-context"

const DESKTOP_BREAKPOINT = 768
import Markdown from "react-native-markdown-display"
import { useChats } from "../hooks/useChats"
import { useVoice } from "../hooks/useVoice"
import { useImagePicker } from "../hooks/useImagePicker"
import { VoiceButton } from "../components/VoiceButton"
import { Message } from "../hooks/useChat"

type Props = {
    token: string | null
    language: string
    provinceState: string
    country: string
    onOpenProfile: () => void
}

export function ChatsScreen({ token, language, provinceState, country, onOpenProfile }: Props) {
    const insets = useSafeAreaInsets()
    const { width } = useWindowDimensions()
    const isDesktop = width >= DESKTOP_BREAKPOINT
    const scrollRef = useRef<ScrollView>(null)
    const [text, setText] = useState("")
    const [chatView, setChatView] = useState<"list" | "detail">("list")

    const {
        chats,
        activeChatId,
        createChat,
        setActiveChatId,
        sendMessageToActiveChat,
        isLoading,
        deleteChat,
    } = useChats({ token, language, provinceState, country })

    const activeChat = chats.find(c => c.id === activeChatId) ?? null
    const messages: Message[] = activeChat?.messages ?? []

    const { isRecording, startRecording, stopRecording } = useVoice(
        sendMessageToActiveChat,
        language ?? "EN",
    )
    const { imageUri, pickImage, uploadImage, clearImage } = useImagePicker()

    useEffect(() => {
        scrollRef.current?.scrollToEnd({ animated: true })
    }, [messages, isLoading])

    async function handleSend() {
        if (!text.trim() && !imageUri) return
        const msg = text
        setText("")
        clearImage()
        const url = await uploadImage()
        await sendMessageToActiveChat(msg, url ?? undefined)
    }

    async function handleSelectChat(id: string) {
        await setActiveChatId(id)
        setChatView("detail")
    }

    async function handleNewChat() {
        await createChat()
        setChatView("detail")
    }

    // ── List view ─────────────────────────────────────────────────────────────

    if (chatView === "list" || !activeChatId) {
        return (
            <View style={[styles.root, { paddingTop: insets.top }]}>
                <View style={[styles.header, isDesktop && styles.headerDesktop]}>
                    <View style={{ flex: 1 }}>
                        <Text style={[styles.headerTitle, isDesktop && styles.headerTitleDesktop]}>
                            Chats
                        </Text>
                        <Text style={[styles.headerSub, isDesktop && styles.headerSubDesktop]}>
                            {chats.length} conversation{chats.length !== 1 ? "s" : ""}
                        </Text>
                    </View>
                    {!isDesktop && (
                        <TouchableOpacity onPress={onOpenProfile} style={styles.avatarBtn} activeOpacity={0.7}>
                            <Text style={{ fontSize: 18 }}>👤</Text>
                        </TouchableOpacity>
                    )}
                </View>

                <TouchableOpacity style={styles.newChatBtn} onPress={handleNewChat} activeOpacity={0.8}>
                    <Text style={styles.newChatText}>＋  New Chat</Text>
                </TouchableOpacity>

                <ScrollView style={{ flex: 1 }} showsVerticalScrollIndicator={false}>
                    {chats.length === 0 && (
                        <View style={styles.emptyState}>
                            <Text style={styles.emptyEmoji}>💬</Text>
                            <Text style={styles.emptyTitle}>No chats yet</Text>
                            <Text style={styles.emptySub}>
                                Start a conversation to ask your advisor{"\n"}about crops, diseases, or schemes.
                            </Text>
                        </View>
                    )}

                    {chats.map(chat => {
                        const lastMsg = chat.messages[chat.messages.length - 1]
                        return (
                            <TouchableOpacity
                                key={chat.id}
                                style={[
                                    styles.chatRow,
                                    chat.id === activeChatId && styles.chatRowActive,
                                ]}
                                onPress={() => handleSelectChat(chat.id)}
                                activeOpacity={0.7}
                            >
                                <View style={styles.chatRowIcon}>
                                    <Text style={{ fontSize: 18 }}>🌾</Text>
                                </View>
                                <View style={{ flex: 1 }}>
                                    <Text style={styles.chatTitle} numberOfLines={1}>
                                        {chat.title}
                                    </Text>
                                    {lastMsg && (
                                        <Text style={styles.chatPreview} numberOfLines={1}>
                                            {lastMsg.role === "assistant" ? "🌾 " : "You: "}
                                            {lastMsg.text}
                                        </Text>
                                    )}
                                </View>
                                <TouchableOpacity
                                    onPress={() => deleteChat(chat.id)}
                                    hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
                                    style={styles.deleteBtn}
                                >
                                    <Text style={styles.deleteText}>✕</Text>
                                </TouchableOpacity>
                            </TouchableOpacity>
                        )
                    })}
                </ScrollView>
            </View>
        )
    }

    // ── Detail view ───────────────────────────────────────────────────────────

    return (
        <KeyboardAvoidingView
            style={[styles.root, { paddingTop: insets.top }]}
            behavior={Platform.OS === "ios" ? "padding" : "height"}
        >
            <View style={styles.header}>
                <TouchableOpacity
                    onPress={() => setChatView("list")}
                    hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
                    style={{ marginRight: 10 }}
                >
                    <Text style={styles.backText}>← Back</Text>
                </TouchableOpacity>
                <View style={{ flex: 1 }}>
                    <Text style={styles.headerTitle} numberOfLines={1}>
                        {activeChat?.title ?? "Chat"}
                    </Text>
                </View>
                <Text style={{ fontSize: 26 }}>🌾</Text>
            </View>

            <ScrollView
                ref={scrollRef}
                style={{ flex: 1 }}
                contentContainerStyle={styles.chatContent}
                showsVerticalScrollIndicator={false}
            >
                {messages.length === 0 && (
                    <View style={styles.emptyState}>
                        <Text style={styles.emptyEmoji}>🌱</Text>
                        <Text style={styles.emptyTitle}>Ask your advisor</Text>
                        <Text style={styles.emptySub}>
                            Type a question or press the mic.{"\n"}
                            Ask about crops, diseases, or government schemes.
                        </Text>
                    </View>
                )}

                {messages.map((msg: Message, i: number) => (
                    <View
                        key={i}
                        style={msg.role === "user" ? styles.userRow : styles.assistantRow}
                    >
                        {msg.role === "assistant" && (
                            <Text style={styles.avatar}>🌾</Text>
                        )}
                        <View style={msg.role === "user" ? styles.userBubble : styles.assistantBubble}>
                            {msg.role === "user" ? (
                                <Text style={styles.userText}>{msg.text}</Text>
                            ) : (
                                <Markdown style={mdStyles}>{msg.text}</Markdown>
                            )}
                        </View>
                    </View>
                ))}

                {isLoading && (
                    <View style={styles.assistantRow}>
                        <Text style={styles.avatar}>🌾</Text>
                        <View style={styles.assistantBubble}>
                            <Text style={styles.typingText}>Thinking...</Text>
                        </View>
                    </View>
                )}
            </ScrollView>

            {imageUri && (
                <View style={styles.imagePreviewWrap}>
                    <Image source={{ uri: imageUri }} style={styles.imagePreview} />
                    <TouchableOpacity onPress={clearImage} style={styles.imageClearBtn}>
                        <Text style={styles.imageClearText}>✕</Text>
                    </TouchableOpacity>
                </View>
            )}

            <View style={[styles.inputBar, { paddingBottom: insets.bottom + 10 }]}>
                <TouchableOpacity onPress={pickImage} style={{ padding: 8 }}>
                    <Text style={{ fontSize: 22 }}>📷</Text>
                </TouchableOpacity>
                <TextInput
                    style={styles.input}
                    value={text}
                    onChangeText={setText}
                    placeholder="Ask about your crops..."
                    placeholderTextColor="#8FAF8F"
                    multiline
                    onSubmitEditing={handleSend}
                />
                <Pressable
                    style={({ pressed }) => [styles.sendButton, pressed && styles.sendButtonPressed]}
                    onPress={handleSend}
                >
                    <Text style={styles.sendLabel}>Send</Text>
                </Pressable>
                <VoiceButton
                    isRecording={isRecording}
                    onStart={startRecording}
                    onStop={stopRecording}
                />
            </View>
        </KeyboardAvoidingView>
    )
}

const mdStyles = {
    body: { color: "#1A3A1A", fontSize: 15, lineHeight: 22 },
    heading1: { fontSize: 18, fontWeight: "700" as const, color: "#1B5E20", marginTop: 12, marginBottom: 4 },
    heading2: { fontSize: 16, fontWeight: "700" as const, color: "#2E7D32", marginTop: 10, marginBottom: 4 },
    strong: { fontWeight: "700" as const, color: "#1A3A1A" },
    paragraph: { marginVertical: 4 },
    bullet_list: { marginVertical: 4 },
    code_inline: {
        backgroundColor: "#E8F5E9",
        color: "#1B5E20",
        borderRadius: 4,
        paddingHorizontal: 4,
        fontFamily: "monospace",
    },
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
    backText: { color: "#A5D6A7", fontSize: 14, fontWeight: "600" },

    newChatBtn: {
        margin: 16,
        backgroundColor: "#2E7D32",
        borderRadius: 12,
        padding: 14,
        alignItems: "center",
        borderWidth: 1,
        borderColor: "#43A047",
    },
    newChatText: { color: "#FFFFFF", fontWeight: "700", fontSize: 15 },

    emptyState: {
        alignItems: "center",
        marginTop: 60,
        gap: 10,
        paddingHorizontal: 24,
    },
    emptyEmoji: { fontSize: 52 },
    emptyTitle: { fontSize: 18, fontWeight: "700", color: "#2E7D32" },
    emptySub: { fontSize: 14, color: "#7A9E7A", textAlign: "center", lineHeight: 21 },

    chatRow: {
        flexDirection: "row",
        alignItems: "center",
        paddingHorizontal: 16,
        paddingVertical: 12,
        borderBottomWidth: 1,
        borderBottomColor: "#E8F5E9",
        backgroundColor: "#FFFFFF",
        gap: 10,
    },
    chatRowActive: { backgroundColor: "#E8F5E9" },
    chatRowIcon: {
        width: 40, height: 40, borderRadius: 20,
        backgroundColor: "#E8F5E9",
        alignItems: "center", justifyContent: "center",
    },
    chatTitle: { fontSize: 14, fontWeight: "600", color: "#1A3A1A" },
    chatPreview: { fontSize: 12, color: "#7A9E7A", marginTop: 2 },
    deleteBtn: { padding: 6 },
    deleteText: { color: "#A5D6A7", fontSize: 14 },

    chatContent: { padding: 16, paddingBottom: 8, gap: 12 },

    userRow: { flexDirection: "row", justifyContent: "flex-end" },
    assistantRow: { flexDirection: "row", alignItems: "flex-end", gap: 8 },
    avatar: { fontSize: 22, marginBottom: 4 },

    userBubble: {
        backgroundColor: "#2E7D32",
        borderRadius: 18, borderBottomRightRadius: 4,
        paddingHorizontal: 16, paddingVertical: 10,
        maxWidth: "78%",
    },
    assistantBubble: {
        backgroundColor: "#FFFFFF",
        borderRadius: 18, borderBottomLeftRadius: 4,
        paddingHorizontal: 16, paddingVertical: 10,
        maxWidth: "78%",
        borderLeftWidth: 3, borderLeftColor: "#4CAF50",
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.06, shadowRadius: 2, elevation: 1,
    },
    userText: { color: "#FFFFFF", fontSize: 15, lineHeight: 21 },
    typingText: { color: "#7A9E7A", fontSize: 15, fontStyle: "italic" },

    imagePreviewWrap: { paddingHorizontal: 12, paddingTop: 8 },
    imagePreview: { width: 60, height: 60, borderRadius: 8 },
    imageClearBtn: {
        position: "absolute", top: 4, right: 4,
        backgroundColor: "#F44336",
        borderRadius: 10, paddingHorizontal: 5,
    },
    imageClearText: { color: "#FFFFFF", fontSize: 12 },

    inputBar: {
        flexDirection: "row",
        alignItems: "center",
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
        borderRadius: 22,
        paddingHorizontal: 16, paddingVertical: 10,
        fontSize: 15, color: "#1A3A1A",
        maxHeight: 100,
        borderWidth: 1, borderColor: "#C8E6C9",
    },
    sendButton: {
        backgroundColor: "#2E7D32",
        borderRadius: 22,
        paddingHorizontal: 16, paddingVertical: 10,
    },
    sendButtonPressed: { backgroundColor: "#1B5E20" },
    sendLabel: { color: "#FFFFFF", fontWeight: "bold", fontSize: 15 },
})
