import React, { useState } from "react"
import { View, Text, TextInput, Pressable, StyleSheet, ActivityIndicator } from "react-native"

type Props = {
    onLogin: (email: string, password: string) => Promise<boolean>
    onGoToRegister: () => void
    error: string | null
}

export function LoginScreen({ onLogin, onGoToRegister, error }: Props) {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)

    async function handleLogin() {
        if (!email || !password) return
        setLoading(true)
        await onLogin(email, password)
        setLoading(false)
    }

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Rythu</Text>
            <Text style={styles.subtitle}>Sign in to continue</Text>
            {error && <Text style={styles.error}>{error}</Text>}
            <TextInput
                style={styles.input}
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
            />
            <TextInput
                style={styles.input}
                placeholder="Password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
            />
            <Pressable style={styles.button} onPress={handleLogin} disabled={loading}>
                {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Login</Text>}
            </Pressable>
            <Pressable onPress={onGoToRegister}>
                <Text style={styles.link}>Don't have an account? Register</Text>
            </Pressable>
        </View>
    )
}

const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: "center", alignItems: "center", padding: 24, backgroundColor: "#fff" },
    title: { fontSize: 32, fontWeight: "bold", marginBottom: 4 },
    subtitle: { fontSize: 16, color: "#666", marginBottom: 32 },
    error: { color: "red", marginBottom: 16 },
    input: { width: "100%", maxWidth: 360, borderWidth: 1, borderColor: "#ddd", borderRadius: 8, padding: 12, marginBottom: 12, fontSize: 16 },
    button: { width: "100%", maxWidth: 360, backgroundColor: "#2e7d32", padding: 14, borderRadius: 8, alignItems: "center", marginBottom: 16 },
    buttonText: { color: "#fff", fontSize: 16, fontWeight: "600" },
    link: { color: "#2e7d32", fontSize: 14 },
})
