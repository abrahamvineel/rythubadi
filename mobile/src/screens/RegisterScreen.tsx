import React, { useState } from "react"
import { View, Text, TextInput, Pressable, StyleSheet, ActivityIndicator, TouchableOpacity, ScrollView } from "react-native"

const LANGUAGES = [
    { label: "English", value: "EN" },
    { label: "Telugu", value: "TE" },
    { label: "French", value: "FR" },
]

const REGIONS = [
    { label: "Ontario, Canada", value: "Ontario" },
    { label: "Quebec, Canada", value: "Quebec" },
    { label: "Andhra Pradesh, India", value: "Andhra Pradesh" },
]

type Props = {
    onRegister: (email: string, name: string, password: string, language: string, provinceState: string) => Promise<boolean>
    onGoToLogin: () => void
    error: string | null
}

export function RegisterScreen({ onRegister, onGoToLogin, error }: Props) {
    const [email, setEmail] = useState("")
    const [name, setName] = useState("")
    const [password, setPassword] = useState("")
    const [language, setLanguage] = useState("EN")
    const [provinceState, setProvinceState] = useState("Ontario")
    const [loading, setLoading] = useState(false)

    async function handleRegister() {
        if (!email || !name || !password) return
        setLoading(true)
        await onRegister(email, name, password, language, provinceState)
        setLoading(false)
    }

    return (
        <ScrollView contentContainerStyle={styles.container}>
            <View style={styles.form}>
                <Text style={styles.title}>Rythu</Text>
                <Text style={styles.subtitle}>Create your account</Text>
                {error && <Text style={styles.error}>{error}</Text>}

                <TextInput style={styles.input} placeholder="Full name" value={name} onChangeText={setName} />
                <TextInput style={styles.input} placeholder="Email" value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
                <TextInput style={styles.input} placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry />

                <Text style={styles.label}>Language</Text>
                <View style={styles.optionRow}>
                    {LANGUAGES.map(l => (
                        <TouchableOpacity
                            key={l.value}
                            style={[styles.chip, language === l.value && styles.chipActive]}
                            onPress={() => setLanguage(l.value)}
                        >
                            <Text style={[styles.chipText, language === l.value && styles.chipTextActive]}>{l.label}</Text>
                        </TouchableOpacity>
                    ))}
                </View>

                <Text style={styles.label}>Region</Text>
                <View style={styles.optionRow}>
                    {REGIONS.map(r => (
                        <TouchableOpacity
                            key={r.value}
                            style={[styles.chip, provinceState === r.value && styles.chipActive]}
                            onPress={() => setProvinceState(r.value)}
                        >
                            <Text style={[styles.chipText, provinceState === r.value && styles.chipTextActive]}>
                                {r.label}
                            </Text>
                        </TouchableOpacity>
                    ))}
                </View>

                <Pressable style={styles.button} onPress={handleRegister} disabled={loading}>
                    {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Register</Text>}
                </Pressable>
                <Pressable onPress={onGoToLogin}>
                    <Text style={styles.link}>Already have an account? Login</Text>
                </Pressable>
            </View>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    container: { flexGrow: 1, backgroundColor: "#fff", alignItems: "center", paddingVertical: 40 },
    form: { width: "100%", maxWidth: 400, paddingHorizontal: 24 },
    title: { fontSize: 32, fontWeight: "bold", marginBottom: 4, textAlign: "center" },
    subtitle: { fontSize: 16, color: "#666", marginBottom: 32, textAlign: "center" },
    error: { color: "red", marginBottom: 16, textAlign: "center" },
    input: { borderWidth: 1, borderColor: "#ddd", borderRadius: 8, padding: 12, marginBottom: 12, fontSize: 16 },
    label: { fontSize: 14, fontWeight: "600", color: "#444", marginBottom: 8, marginTop: 4 },
    optionRow: { flexDirection: "row", flexWrap: "wrap", marginBottom: 16 },
    chip: { paddingHorizontal: 14, paddingVertical: 8, borderRadius: 20, borderWidth: 1, borderColor: "#ccc", backgroundColor: "#f5f5f5", marginRight: 8, marginBottom: 8 },
    chipActive: { backgroundColor: "#2e7d32", borderColor: "#2e7d32" },
    chipText: { fontSize: 14, color: "#444" },
    chipTextActive: { color: "#fff", fontWeight: "600" },
    button: { backgroundColor: "#2e7d32", padding: 14, borderRadius: 8, alignItems: "center", marginBottom: 16, marginTop: 8 },
    buttonText: { color: "#fff", fontSize: 16, fontWeight: "600" },
    link: { color: "#2e7d32", fontSize: 14, textAlign: "center" },
})
