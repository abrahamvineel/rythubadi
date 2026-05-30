import React, { useState } from "react"
import {
    View, Text, TextInput, Pressable, StyleSheet,
    ActivityIndicator, TouchableOpacity, ScrollView, KeyboardAvoidingView, Platform, Alert,
} from "react-native"
import { useSafeAreaInsets } from "react-native-safe-area-context"
import { PRODUCER_TYPES } from "../constants/producerTypes"
import { CountryPicker } from "../components/CountryPicker"

const LANGUAGES = [
    { label: "English", value: "EN" },
    { label: "Telugu",  value: "TE" },
    { label: "French",  value: "FR" },
]

type Props = {
    onRegister: (
        email: string,
        name: string,
        password: string,
        language: string,
        country: string,
        producerTypes: string[],
    ) => Promise<boolean>
    onGoToLogin: () => void
    error: string | null
}

export function RegisterScreen({ onRegister, onGoToLogin, error }: Props) {
    const insets = useSafeAreaInsets()
    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [showPassword, setShowPassword] = useState(false)
    const [language, setLanguage] = useState("EN")
    const [country, setCountry] = useState("CA")
    const [producerTypes, setProducerTypes] = useState<string[]>([])
    const [loading, setLoading] = useState(false)

    function toggleType(value: string) {
        setProducerTypes(prev =>
            prev.includes(value) ? prev.filter(t => t !== value) : [...prev, value]
        )
    }

    const canSubmit = name.trim() && email.trim() && password.length >= 6 && producerTypes.length > 0

    function missingFields(): string | null {
        if (!name.trim()) return "Enter your full name"
        if (!email.trim()) return "Enter your email"
        if (password.length < 6) return "Password must be at least 6 characters"
        if (producerTypes.length === 0) return "Select at least one producer type"
        return null
    }

    async function handleRegister() {
        const missing = missingFields()
        if (missing) {
            // On web use alert since Alert.alert needs native context
            if (Platform.OS === "web") { window.alert(missing); return }
            Alert.alert("Almost there", missing)
            return
        }
        setLoading(true)
        await onRegister(email.trim(), name.trim(), password, language, country, producerTypes)
        setLoading(false)
    }

    return (
        <KeyboardAvoidingView
            style={styles.root}
            behavior={Platform.OS === "ios" ? "padding" : "height"}
        >
            <ScrollView
                contentContainerStyle={[styles.scroll, { paddingTop: insets.top + 16, paddingBottom: insets.bottom + 24 }]}
                keyboardShouldPersistTaps="handled"
            >
                {/* Brand */}
                <View style={styles.brand}>
                    <View style={styles.logoCircle}>
                        <Text style={styles.logoEmoji}>🌾</Text>
                    </View>
                    <Text style={styles.appName}>Rythu</Text>
                    <Text style={styles.tagline}>Create your account</Text>
                </View>

                <View style={styles.card}>
                    {error && (
                        <View style={styles.errorBox}>
                            <Text style={styles.errorText}>⚠ {error}</Text>
                        </View>
                    )}

                    {/* Details */}
                    <Text style={styles.sectionTitle}>Your details</Text>

                    <Text style={styles.fieldLabel}>Full name</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="e.g. Ravi Kumar"
                        placeholderTextColor="#aaa"
                        value={name}
                        onChangeText={setName}
                        autoCapitalize="words"
                    />

                    <Text style={styles.fieldLabel}>Email</Text>
                    <TextInput
                        style={styles.input}
                        placeholder="you@example.com"
                        placeholderTextColor="#aaa"
                        value={email}
                        onChangeText={setEmail}
                        autoCapitalize="none"
                        keyboardType="email-address"
                    />

                    <Text style={styles.fieldLabel}>Password</Text>
                    <View style={styles.passwordRow}>
                        <TextInput
                            style={[styles.input, styles.passwordInput]}
                            placeholder="At least 6 characters"
                            placeholderTextColor="#aaa"
                            value={password}
                            onChangeText={setPassword}
                            secureTextEntry={!showPassword}
                        />
                        <TouchableOpacity style={styles.eyeButton} onPress={() => setShowPassword(v => !v)}>
                            <Text style={styles.eyeIcon}>{showPassword ? "🙈" : "👁"}</Text>
                        </TouchableOpacity>
                    </View>
                    {password.length > 0 && password.length < 6 && (
                        <View style={styles.passwordHintBanner}>
                            <Text style={styles.passwordHintText}>
                                {password.length}/6 characters — {6 - password.length} more needed
                            </Text>
                            <View style={styles.passwordStrengthBar}>
                                <View style={[styles.passwordStrengthFill, { width: `${(password.length / 6) * 100}%` }]} />
                            </View>
                        </View>
                    )}

                    <View style={styles.divider} />

                    {/* What do you produce */}
                    <Text style={styles.sectionTitle}>What do you produce?</Text>
                    <Text style={styles.sectionHint}>Select all that apply — you can add more later</Text>

                    <View style={styles.typeGrid}>
                        {PRODUCER_TYPES.map(pt => {
                            const selected = producerTypes.includes(pt.value)
                            return (
                                <TouchableOpacity
                                    key={pt.value}
                                    style={[styles.typeCard, selected && styles.typeCardActive]}
                                    onPress={() => toggleType(pt.value)}
                                    activeOpacity={0.75}
                                >
                                    <Text style={styles.typeEmoji}>{pt.emoji}</Text>
                                    <Text style={[styles.typeLabel, selected && styles.typeLabelActive]}>
                                        {pt.label}
                                    </Text>
                                    {selected && <Text style={styles.typeCheck}>✓</Text>}
                                </TouchableOpacity>
                            )
                        })}
                    </View>

                    {producerTypes.length === 0 && (
                        <Text style={styles.typeHint}>Select at least one to continue</Text>
                    )}

                    <View style={styles.divider} />

                    {/* Preferences */}
                    <Text style={styles.sectionTitle}>Preferences</Text>

                    <Text style={styles.fieldLabel}>Language</Text>
                    <View style={styles.chipRow}>
                        {LANGUAGES.map(l => (
                            <TouchableOpacity
                                key={l.value}
                                style={[styles.chip, language === l.value && styles.chipActive]}
                                onPress={() => setLanguage(l.value)}
                            >
                                <Text style={[styles.chipText, language === l.value && styles.chipTextActive]}>
                                    {l.label}
                                </Text>
                            </TouchableOpacity>
                        ))}
                    </View>

                    <Text style={styles.fieldLabel}>Country</Text>
                    <CountryPicker value={country} onChange={setCountry} />

                    <Pressable
                        style={[styles.primaryButton, !canSubmit && styles.primaryButtonDisabled]}
                        onPress={handleRegister}
                        disabled={loading}
                    >
                        {loading
                            ? <ActivityIndicator color="#fff" />
                            : <Text style={styles.primaryButtonText}>Create Account</Text>
                        }
                    </Pressable>
                </View>

                <View style={styles.footer}>
                    <Text style={styles.footerText}>Already have an account? </Text>
                    <TouchableOpacity onPress={onGoToLogin}>
                        <Text style={styles.footerLink}>Sign in</Text>
                    </TouchableOpacity>
                </View>
            </ScrollView>
        </KeyboardAvoidingView>
    )
}

const styles = StyleSheet.create({
    root: { flex: 1, backgroundColor: "#F4F9F4" },
    scroll: { flexGrow: 1, alignItems: "center", paddingHorizontal: 20 },

    brand: { alignItems: "center", marginBottom: 24 },
    logoCircle: {
        width: 64, height: 64, borderRadius: 32, backgroundColor: "#1B5E20",
        alignItems: "center", justifyContent: "center", marginBottom: 10,
        shadowColor: "#1B5E20", shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3, shadowRadius: 8, elevation: 6,
    },
    logoEmoji: { fontSize: 30 },
    appName: { fontSize: 28, fontWeight: "800", color: "#1B5E20", letterSpacing: 1 },
    tagline: { fontSize: 13, color: "#6A9A6A", marginTop: 2 },

    card: {
        width: "100%", maxWidth: 440, backgroundColor: "#fff",
        borderRadius: 20, padding: 24,
        shadowColor: "#000", shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.08, shadowRadius: 12, elevation: 3, marginBottom: 24,
    },

    errorBox: {
        backgroundColor: "#FFF3F3", borderRadius: 10, padding: 12,
        marginBottom: 16, borderLeftWidth: 3, borderLeftColor: "#E53935",
    },
    errorText: { color: "#C62828", fontSize: 13 },

    sectionTitle: { fontSize: 15, fontWeight: "700", color: "#1B5E20", marginBottom: 4, marginTop: 4 },
    sectionHint: { fontSize: 12, color: "#888", marginBottom: 14 },
    divider: { height: 1, backgroundColor: "#E8F5E9", marginVertical: 20 },

    fieldLabel: { fontSize: 13, fontWeight: "600", color: "#444", marginBottom: 6, marginTop: 2 },
    input: {
        borderWidth: 1.5, borderColor: "#E0EDE0", borderRadius: 12,
        paddingHorizontal: 14, paddingVertical: 12,
        fontSize: 15, color: "#1A3A1A", backgroundColor: "#FAFFFE", marginBottom: 14,
    },
    passwordRow: { position: "relative", marginBottom: 14 },
    passwordInput: { marginBottom: 0, paddingRight: 48 },
    eyeButton: { position: "absolute", right: 14, top: 12 },
    eyeIcon: { fontSize: 18 },

    passwordHintBanner: {
        backgroundColor: "#FFF8E1",
        borderRadius: 8,
        paddingHorizontal: 12,
        paddingVertical: 8,
        marginTop: -8,
        marginBottom: 14,
        gap: 6,
    },
    passwordHintText: {
        fontSize: 12,
        color: "#E65100",
        fontWeight: "600",
    },
    passwordStrengthBar: {
        height: 3,
        backgroundColor: "#FFE082",
        borderRadius: 2,
        overflow: "hidden",
    },
    passwordStrengthFill: {
        height: "100%",
        backgroundColor: "#E65100",
        borderRadius: 2,
    },

    typeGrid: { flexDirection: "row", flexWrap: "wrap", gap: 10, marginBottom: 8 },
    typeCard: {
        width: "47%", borderRadius: 14, borderWidth: 1.5, borderColor: "#D8EDD8",
        backgroundColor: "#F8FBF8", padding: 14,
        alignItems: "center", justifyContent: "center", minHeight: 80, position: "relative",
    },
    typeCardActive: { borderColor: "#2E7D32", backgroundColor: "#E8F5E9" },
    typeEmoji: { fontSize: 28, marginBottom: 6 },
    typeLabel: { fontSize: 13, fontWeight: "600", color: "#555", textAlign: "center" },
    typeLabelActive: { color: "#1B5E20" },
    typeCheck: { position: "absolute", top: 8, right: 10, fontSize: 13, color: "#2E7D32", fontWeight: "700" },
    typeHint: { fontSize: 12, color: "#E53935", marginBottom: 4 },

    chipRow: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 16 },
    chip: {
        paddingHorizontal: 14, paddingVertical: 8, borderRadius: 20,
        borderWidth: 1.5, borderColor: "#D0E8D0", backgroundColor: "#F4F9F4",
    },
    chipActive: { backgroundColor: "#2E7D32", borderColor: "#2E7D32" },
    chipText: { fontSize: 13, color: "#555", fontWeight: "500" },
    chipTextActive: { color: "#fff", fontWeight: "700" },

    primaryButton: {
        backgroundColor: "#2E7D32", borderRadius: 12,
        paddingVertical: 14, alignItems: "center", marginTop: 8,
    },
    primaryButtonDisabled: { backgroundColor: "#A5D6A7" },
    primaryButtonText: { color: "#fff", fontSize: 16, fontWeight: "700" },

    footer: { flexDirection: "row", alignItems: "center" },
    footerText: { fontSize: 14, color: "#666" },
    footerLink: { fontSize: 14, color: "#2E7D32", fontWeight: "700" },
})
