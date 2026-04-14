import React from "react"
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from "react-native"
import { Chat } from "../hooks/useChats"

type Props = {
    chats: Chat[]
    activeChatId: string | null
    onSelectChat: (id: string) => void
    onNewChat: () => void
    onDeleteChat: (id: string) => void
}

export function Sidebar({ chats, activeChatId, onSelectChat, onNewChat, onDeleteChat }: Props) {
    return (
        <View style={styles.container}>
            <TouchableOpacity style={styles.newChatButton} onPress={onNewChat}>
                <Text style={styles.newChatText}>+ New Chat</Text>
            </TouchableOpacity>
            <ScrollView>
                {chats.map(chat => (
                    <View key={chat.id} style={chat.id === activeChatId ? styles.activeItemRow : styles.itemRow}>
                        <TouchableOpacity style={{ flex: 1 }} onPress={() => onSelectChat(chat.id)}>
                            <Text style={styles.itemText} numberOfLines={1}>{chat.title}</Text>
                        </TouchableOpacity>
                        <TouchableOpacity onPress={() => onDeleteChat(chat.id)}>
                            <Text style={styles.deleteText}>✕</Text>
                        </TouchableOpacity>
                    </View>
                ))}
            </ScrollView>
        </View>
    )
}

const styles = StyleSheet.create({
    container: { width: 220, backgroundColor: "#1B5E20", paddingTop: 60, paddingBottom: 16 },
    newChatButton: { marginHorizontal: 12, marginBottom: 12, backgroundColor: "#2E7D32", borderRadius: 8, padding: 12 },
    newChatText: { color: "#FFFFFF", fontWeight: "bold", fontSize: 14 },
    itemRow: { flexDirection: "row", alignItems: "center", paddingHorizontal: 8, paddingVertical: 4 },
    activeItemRow: { flexDirection: "row", alignItems: "center", paddingHorizontal: 8, paddingVertical: 4, backgroundColor: "#2E7D32", borderRadius: 8, marginHorizontal: 4 },
    itemText: { color: "#C8E6C9", fontSize: 14, paddingVertical: 8, paddingHorizontal: 8 },
    deleteText: { color: "#A5D6A7", fontSize: 12, paddingHorizontal: 6 },
})
