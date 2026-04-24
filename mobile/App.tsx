import React, { useState, useRef, useEffect } from "react"
import { useAuth } from "./src/hooks/useAuth"
import { LoginScreen } from "./src/screens/LoginScreen"
import { RegisterScreen } from "./src/screens/RegisterScreen"
import {
    StyleSheet,
    Text,
    View,
    ScrollView,
    TextInput,
    Pressable,
    KeyboardAvoidingView,
    Platform,
    TouchableOpacity,
    Image,
} from "react-native"
import { useChats } from "./src/hooks/useChats"
import { Message } from "./src/hooks/useChat"
import { useVoice } from "./src/hooks/useVoice"
import { VoiceButton } from "./src/components/VoiceButton"
import { Sidebar } from "./src/components/SideBar"
import { useImagePicker } from "./src/hooks/useImagePicker"
import Markdown from "react-native-markdown-display"

export default function App() {
    const { token, name, language, provinceState, country, loading: authLoading, error: authError, login, register, logout } = useAuth()
    const [authScreen, setAuthScreen] = useState<"login" | "register">("login")
    const { chats, activeChatId, createChat, setActiveChatId, sendMessageToActiveChat, isLoading, deleteChat } = useChats({ language, provinceState, country })
    const [sidebarOpen, setSidebarOpen] = useState(true)
    const [text, setText] = useState("")
    const scrollRef = useRef<ScrollView>(null)
    const activeChat = chats.find(c => c.id === activeChatId) ?? null
    const messages = activeChat?.messages ?? []
    const { isRecording, startRecording, stopRecording } = useVoice(sendMessageToActiveChat, language ?? "EN")
    const { imageUri, pickImage, uploadImage, clearImage } = useImagePicker()

    useEffect(() => {
        scrollRef.current?.scrollToEnd({ animated: true })
    }, [messages, isLoading])

    if (authLoading) return null

    if (!token) {
        if (authScreen === "register")
            return <RegisterScreen onRegister={register} onGoToLogin={() => setAuthScreen("login")} error={authError} />
        return <LoginScreen onLogin={login} onGoToRegister={() => setAuthScreen("register")} error={authError} />
    }

    async function handleSend() {
        if (!text.trim() && !imageUri) return
        const message = text
        setText("")
        clearImage()
        const uploadedUrl = await uploadImage()
        await sendMessageToActiveChat(message, uploadedUrl ?? undefined)
    }

    return (
        <KeyboardAvoidingView
            style={styles.root}
            behavior={Platform.OS === "ios" ? "padding" : "height"}
        >
            {/* Header */}
            <View style={styles.header}>
                    <TouchableOpacity onPress={() => setSidebarOpen(o => !o)} style={{ marginRight: 12 }}>
                        <Text style={{ color: "#fff", fontSize: 20 }}>☰</Text>
                    </TouchableOpacity>
                    <Text style={styles.headerEmoji}>🌾</Text>
                    <View style={{ flex: 1 }}>
                        <Text style={styles.headerTitle}>Rythu Voice</Text>
                        <Text style={styles.headerSubtitle}>Your AI farming advisor</Text>
                    </View>
            </View>

            {/* Body: sidebar + chat */}
            <View style={{ flex: 1, flexDirection: "row" }}>
                {sidebarOpen && (
                    <Sidebar
                        chats={chats}
                        activeChatId={activeChatId}
                        onSelectChat={setActiveChatId}
                        onNewChat={createChat}
                        onDeleteChat={deleteChat}
                        name={name}
                        language={language}
                        provinceState={provinceState}
                        onLogout={logout}
                    />
                )}

                {/* Chat area + input bar */}
                <View style={{ flex: 1 }}>
            <ScrollView
                ref={scrollRef}
                style={styles.chatArea}
                contentContainerStyle={styles.chatContent}
            >
                {messages.length === 0 && (
                    <View style={styles.emptyState}>
                        <Text style={styles.emptyEmoji}>🌱</Text>
                        <Text style={styles.emptyTitle}>Ask your advisor</Text>
                        <Text style={styles.emptySubtitle}>
                            Type a question or press the mic to speak.{"\n"}
                            Ask about crops, diseases, or government schemes.
                        </Text>
                    </View>
                )}

                {messages.map((msg: Message, index: number) => (
                    <View
                        key={index}
                        style={msg.role === "user" ? styles.userRow : styles.assistantRow}
                    >
                        {msg.role === "assistant" && (
                            <Text style={styles.avatar}>🌾</Text>
                        )}
                        <View style={msg.role === "user" ? styles.userBubble : styles.assistantBubble}>
                            {msg.role === "user" ? (
                                <Text style={styles.userText}>{msg.text}</Text>
                            ) : (
                                <Markdown style={markdownStyles}>{msg.text}</Markdown>
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
                <View style={{ paddingHorizontal: 12, paddingTop: 8 }}>
                    <Image source={{ uri: imageUri }} style={{ width: 60, height: 60, borderRadius: 8 }} />
                    <TouchableOpacity onPress={clearImage} style={{ position: "absolute", top: 4, right: 4 }}>
                        <Text style={{ color: "#fff", backgroundColor: "#F44336", borderRadius: 10, paddingHorizontal: 5 }}>✕</Text>
                    </TouchableOpacity>
                </View>
            )}


            {/* Input bar */}
            <View style={styles.inputBar}>
                
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
            </View>
            </View>
        </KeyboardAvoidingView>
    )
}

const markdownStyles = {
    body: { color: "#1A3A1A", fontSize: 15, lineHeight: 22 },
    heading1: { fontSize: 18, fontWeight: "700" as const, color: "#1B5E20", marginTop: 12, marginBottom: 4 },
    heading2: { fontSize: 16, fontWeight: "700" as const, color: "#2E7D32", marginTop: 10, marginBottom: 4 },
    heading3: { fontSize: 15, fontWeight: "600" as const, color: "#2E7D32", marginTop: 8, marginBottom: 2 },
    strong: { fontWeight: "700" as const, color: "#1A3A1A" },
    bullet_list: { marginVertical: 4 },
    bullet_list_item: { flexDirection: "row" as const },
    bullet_list_icon: { color: "#4CAF50", marginRight: 6 },
    ordered_list_item: { flexDirection: "row" as const },
    code_inline: { backgroundColor: "#E8F5E9", color: "#1B5E20", borderRadius: 4, paddingHorizontal: 4, fontFamily: "monospace" },
    fence: { backgroundColor: "#E8F5E9", padding: 10, borderRadius: 8, marginVertical: 6 },
    blockquote: { borderLeftWidth: 3, borderLeftColor: "#4CAF50", paddingLeft: 10, marginVertical: 4, opacity: 0.85 },
    hr: { backgroundColor: "#C8E6C9", height: 1, marginVertical: 8 },
    paragraph: { marginVertical: 4 },
}

const styles = StyleSheet.create({
    root: {
        flex: 1,
        backgroundColor: "#F4F9F4",
    },

    // Header
    header: {
        backgroundColor: "#1B5E20",
        paddingTop: 60,
        paddingBottom: 16,
        paddingHorizontal: 20,
        flexDirection: "row",
        alignItems: "center",
        gap: 12,
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.15,
        shadowRadius: 4,
        elevation: 4,
    },
    headerEmoji: {
        fontSize: 32,
    },
    headerTitle: {
        fontSize: 22,
        fontWeight: "bold",
        color: "#FFFFFF",
    },
    headerSubtitle: {
        fontSize: 13,
        color: "#A5D6A7",
        marginTop: 2,
    },

    // Chat area
    chatArea: {
        flex: 1,
    },
    chatContent: {
        padding: 16,
        paddingBottom: 8,
        gap: 12,
    },

    // Empty state
    emptyState: {
        alignItems: "center",
        marginTop: 60,
        gap: 12,
    },
    emptyEmoji: {
        fontSize: 48,
    },
    emptyTitle: {
        fontSize: 20,
        fontWeight: "bold",
        color: "#2E7D32",
    },
    emptySubtitle: {
        fontSize: 15,
        color: "#7A9E7A",
        textAlign: "center",
        lineHeight: 22,
    },

    // Message rows
    userRow: {
        flexDirection: "row",
        justifyContent: "flex-end",
    },
    assistantRow: {
        flexDirection: "row",
        alignItems: "flex-end",
        gap: 8,
    },
    avatar: {
        fontSize: 22,
        marginBottom: 4,
    },

    // Bubbles
    userBubble: {
        backgroundColor: "#2E7D32",
        borderRadius: 18,
        borderBottomRightRadius: 4,
        paddingHorizontal: 16,
        paddingVertical: 10,
        maxWidth: "78%",
    },
    assistantBubble: {
        backgroundColor: "#FFFFFF",
        borderRadius: 18,
        borderBottomLeftRadius: 4,
        paddingHorizontal: 16,
        paddingVertical: 10,
        maxWidth: "78%",
        borderLeftWidth: 3,
        borderLeftColor: "#4CAF50",
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.06,
        shadowRadius: 2,
        elevation: 1,
    },
    userText: {
        color: "#FFFFFF",
        fontSize: 15,
        lineHeight: 21,
    },
    assistantText: {
        color: "#1A3A1A",
        fontSize: 15,
        lineHeight: 21,
    },
    typingText: {
        color: "#7A9E7A",
        fontSize: 15,
        fontStyle: "italic",
    },

    // Input bar
    inputBar: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: "#FFFFFF",
        paddingHorizontal: 12,
        paddingVertical: 10,
        paddingBottom: 28,
        gap: 8,
        borderTopWidth: 1,
        borderTopColor: "#D8EDD8",
    },
    input: {
        flex: 1,
        backgroundColor: "#F0F7F0",
        borderRadius: 22,
        paddingHorizontal: 16,
        paddingVertical: 10,
        fontSize: 15,
        color: "#1A3A1A",
        maxHeight: 100,
        borderWidth: 1,
        borderColor: "#C8E6C9",
    },
    sendButton: {
        backgroundColor: "#2E7D32",
        borderRadius: 22,
        paddingHorizontal: 16,
        paddingVertical: 10,
    },
    sendButtonPressed: {
        backgroundColor: "#1B5E20",
    },
    sendLabel: {
        color: "#FFFFFF",
        fontWeight: "bold",
        fontSize: 15,
    },
})
