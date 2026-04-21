import React from "react"
import { View, Text, TouchableOpacity, StyleSheet, ScrollView } from "react-native"
import { Chat } from "../hooks/useChats"

type Props = {
    chats: Chat[]
    activeChatId: string | null
    onSelectChat: (id: string) => void
    onNewChat: () => void
    onDeleteChat: (id: string) => void
    name: string | null
    language: string
    provinceState: string
    onLogout: () => void
}

export function Sidebar({ chats, activeChatId, onSelectChat, onNewChat, onDeleteChat, name, language, provinceState, onLogout }: Props) {
    const initials = name ? name.split(" ").map(w => w[0]).join("").toUpperCase().slice(0, 2) : "?"

    return (
        <View style={styles.container}>
            {/* App label */}
            <View style={styles.brandRow}>
                <Text style={styles.brandEmoji}>🌾</Text>
                <Text style={styles.brandText}>Rythu</Text>
            </View>

            <TouchableOpacity style={styles.newChatButton} onPress={onNewChat}>
                <Text style={styles.newChatText}>＋  New Chat</Text>
            </TouchableOpacity>

            <Text style={styles.sectionLabel}>RECENT</Text>

            <ScrollView style={{ flex: 1 }}>
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

            {/* Profile section */}
            <View style={styles.profileSection}>
                <View style={styles.avatar}>
                    <Text style={styles.avatarText}>{initials}</Text>
                </View>
                <View style={{ flex: 1 }}>
                    <Text style={styles.profileName} numberOfLines={1}>{name ?? "User"}</Text>
                    <Text style={styles.profileSub}>{language} · {provinceState}</Text>
                </View>
                <TouchableOpacity onPress={onLogout} style={styles.logoutBtn}>
                    <Text style={styles.logoutText}>⏻</Text>
                </TouchableOpacity>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    container: { width: 240, backgroundColor: "#1B5E20", paddingTop: 52, paddingBottom: 0, flexDirection: "column" },
    brandRow: { flexDirection: "row", alignItems: "center", paddingHorizontal: 16, marginBottom: 16 },
    brandEmoji: { fontSize: 20, marginRight: 8 },
    brandText: { color: "#FFFFFF", fontSize: 18, fontWeight: "700", letterSpacing: 1 },
    newChatButton: { marginHorizontal: 12, marginBottom: 16, backgroundColor: "#2E7D32", borderRadius: 10, padding: 12, borderWidth: 1, borderColor: "#43A047" },
    newChatText: { color: "#FFFFFF", fontWeight: "600", fontSize: 14, textAlign: "center" },
    sectionLabel: { color: "#81C784", fontSize: 10, fontWeight: "700", letterSpacing: 1.2, paddingHorizontal: 16, marginBottom: 4 },
    itemRow: { flexDirection: "row", alignItems: "center", paddingHorizontal: 8, paddingVertical: 2, marginHorizontal: 4, borderRadius: 8 },
    activeItemRow: { flexDirection: "row", alignItems: "center", paddingHorizontal: 8, paddingVertical: 2, backgroundColor: "#2E7D32", borderRadius: 8, marginHorizontal: 4 },
    itemText: { color: "#C8E6C9", fontSize: 13, paddingVertical: 8, paddingHorizontal: 4 },
    deleteText: { color: "#A5D6A7", fontSize: 12, paddingHorizontal: 6 },
    profileSection: { flexDirection: "row", alignItems: "center", padding: 12, borderTopWidth: 1, borderTopColor: "#2E7D32", backgroundColor: "#163d17" },
    avatar: { width: 36, height: 36, borderRadius: 18, backgroundColor: "#43A047", alignItems: "center", justifyContent: "center", marginRight: 10 },
    avatarText: { color: "#fff", fontWeight: "700", fontSize: 14 },
    profileName: { color: "#FFFFFF", fontSize: 13, fontWeight: "600" },
    profileSub: { color: "#81C784", fontSize: 11 },
    logoutBtn: { padding: 6 },
    logoutText: { color: "#81C784", fontSize: 18 },
})
