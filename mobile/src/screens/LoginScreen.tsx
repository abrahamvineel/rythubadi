import React, { useState } from "react"
import {
    View, Text, TextInput, Pressable, StyleSheet,
    ActivityIndicator, KeyboardAvoidingView, Platform,
    TouchableOpacity, ScrollView,
} from "react-native"
import { useSafeAreaInsets } from "react-native-safe-area-context"

type Props = {
    onLogin: (email: string, password: string) => Promise<boolean>
    onGoToRegister: () => void
    error: string | null
}

export function LoginScreen({ onLogin, onGoToRegister, error }: Props) {
    const insets = useSafeAreaInsets()
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const [showPassword, setShowPassword] = useState(false)

    async function handleLogin() {
        if (!email.trim() || !password) return
        setLoading(true)
        await onLogin(email.trim(), password)
        setLoading(false)
    }

    const canSubmit = email.trim().length > 0 && password.length > 0

    return (
        <KeyboardAvoidingView
            style={styles.root}
            behavior={Platform.OS === "ios" ? "padding" : "height"}
        >
            <ScrollView
                contentContainerStyle={[styles.scroll, { paddingTop: insets.top + 24, paddingBottom: insets.bottom + 24 }]}
                keyboardShouldPersistTaps="handled"
            >
                {/* Brand */}
                <View style={styles.brand}>
                    <View style={styles.logoCircle}>
                        <Text style={styles.logoEmoji}>🌾</Text>
                    </View>
                    <Text style={styles.appName}>Rythu</Text>
                    <Text style={styles.tagline}>Your AI farming advisor</Text>
                </View>

                {/* Card */}
                <View style={styles.card}>
                    <Text style={styles.cardTitle}>Welcome back</Text>
                    <Text style={styles.cardSubtitle}>Sign in to continue</Text>

                    {error && (
                        <View style={styles.errorBox}>
                            <Text style={styles.errorText}>⚠ {error}</Text>
                        </View>
                    )}

                    <Text style={styles.fieldLabel}>Email</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="you@example.com"
                        placeholderTextColor="#aaa"
                        value={email}
                        onChangeText={setEmail}
                        autoCapitalize="none"
                        keyboardType="email-address"
                        autoComplete="email"
                    />

                    <Text style={styles.fieldLabel}>Password</Text>
                    <View style={styles.passwordRow}>
                        <TextInput
                            style={[styles.input, styles.passwordInput]}
                            placeholder="Your password"
                            placeholderTextColor="#aaa"
                            value={password}
                            onChangeText={setPassword}
                            secureTextEntry={!showPassword}
                        />
                        <TouchableOpacity
                            style={styles.eyeButton}
                            onPress={() => setShowPassword(v => !v)}
                        >
                            <Text style={styles.eyeIcon}>{showPassword ? "🙈" : "👁"}</Text>
                        </TouchableOpacity>
                    </View>

                    <Pressable
                        style={[styles.primaryButton, !canSubmit && styles.primaryButtonDisabled]}
                        onPress={handleLogin}
                        disabled={loading || !canSubmit}
                    >
                        {loading
                            ? <ActivityIndicator color="#fff" />
                            : <Text style={styles.primaryButtonText}>Sign In</Text>
                        }
                    </Pressable>
                </View>

                {/* Footer */}
                <View style={styles.footer}>
                    <Text style={styles.footerText}>Don't have an account? </Text>
                    <TouchableOpacity onPress={onGoToRegister}>
                        <Text style={styles.footerLink}>Create one</Text>
                    </TouchableOpacity>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    )
}

const styles = StyleSheet.create({
    root: { flex: 1, backgroundColor: "#F4F9F4" },
    scroll: { flexGrow: 1, alignItems: "center", paddingHorizontal: 24 },

    // Brand
    brand: { alignItems: "center", marginBottom: 32 },
    logoCircle: {
        width: 80, height: 80, borderRadius: 40,
        backgroundColor: "#1B5E20",
        alignItems: "center", justifyContent: "center",
        marginBottom: 12,
        shadowColor: "#1B5E20", shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3, shadowRadius: 8, elevation: 6,
    },
    logoEmoji: { fontSize: 38 },
    appName: { fontSize: 34, fontWeight: "800", color: "#1B5E20", letterSpacing: 1 },
    tagline: { fontSize: 14, color: "#6A9A6A", marginTop: 4 },

    // Card
    card: {
        width: "100%", maxWidth: 420,
        backgroundColor: "#fff",
        borderRadius: 20,
        padding: 24,
        shadowColor: "#000", shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.08, shadowRadius: 12, elevation: 3,
        marginBottom: 24,
    },
    cardTitle: { fontSize: 22, fontWeight: "700", color: "#1A3A1A", marginBottom: 4 },
    cardSubtitle: { fontSize: 14, color: "#888", marginBottom: 20 },

    errorBox: {
        backgroundColor: "#FFF3F3", borderRadius: 10, padding: 12,
        marginBottom: 16, borderLeftWidth: 3, borderLeftColor: "#E53935",
    },
    errorText: { color: "#C62828", fontSize: 13 },

    fieldLabel: { fontSize: 13, fontWeight: "600", color: "#444", marginBottom: 6, marginTop: 4 },
    input: {
        borderWidth: 1.5, borderColor: "#E0EDE0", borderRadius: 12,
        paddingHorizontal: 14, paddingVertical: 12,
        fontSize: 15, color: "#1A3A1A", backgroundColor: "#FAFFFE",
        marginBottom: 16,
    },
    passwordRow: { position: "relative", marginBottom: 16 },
    passwordInput: { marginBottom: 0, paddingRight: 48 },
    eyeButton: { position: "absolute", right: 14, top: 12 },
    eyeIcon: { fontSize: 18 },

    primaryButton: {
        backgroundColor: "#2E7D32", borderRadius: 12,
        paddingVertical: 14, alignItems: "center", marginTop: 4,
    },
    primaryButtonDisabled: { backgroundColor: "#A5D6A7" },
    primaryButtonText: { color: "#fff", fontSize: 16, fontWeight: "700" },

    // Footer
    footer: { flexDirection: "row", alignItems: "center" },
    footerText: { fontSize: 14, color: "#666" },
    footerLink: { fontSize: 14, color: "#2E7D32", fontWeight: "700" },
})
