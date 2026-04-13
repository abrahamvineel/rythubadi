import React, { useState, useRef, useEffect } from "react"
import {
    StyleSheet,
    Text,
    View,
    ScrollView,
    TextInput,
    Pressable,
    KeyboardAvoidingView,
    Platform,
} from "react-native"
import { useChat, Message } from "./src/hooks/useChat"
import { useVoice } from "./src/hooks/useVoice"
import { VoiceButton } from "./src/components/VoiceButton"

export default function App() {
    const { messages, isLoading, sendMessage } = useChat()
    const { isRecording, startRecording, stopRecording } = useVoice(sendMessage)
    const [text, setText] = useState("")
    const scrollRef = useRef<ScrollView>(null)

    useEffect(() => {
        scrollRef.current?.scrollToEnd({ animated: true })
    }, [messages, isLoading])

    function handleSend() {
        if (!text.trim()) return
        sendMessage(text)
        setText("")
    }

    return (
        <KeyboardAvoidingView
            style={styles.root}
            behavior={Platform.OS === "ios" ? "padding" : "height"}
        >
            {/* Header */}
            <View style={styles.header}>
                <Text style={styles.headerEmoji}>🌾</Text>
                <View>
                    <Text style={styles.headerTitle}>Rythu Voice</Text>
                    <Text style={styles.headerSubtitle}>Your AI farming advisor</Text>
                </View>
            </View>

            {/* Chat area */}
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
                            <Text style={msg.role === "user" ? styles.userText : styles.assistantText}>
                                {msg.text}
                            </Text>
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

            {/* Input bar */}
            <View style={styles.inputBar}>
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
