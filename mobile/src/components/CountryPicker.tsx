import React, { useState } from "react"
import {
    Modal, View, Text, TextInput, TouchableOpacity,
    FlatList, StyleSheet, Pressable,
} from "react-native"
import { COUNTRIES, Country } from "../constants/regions"

type Props = {
    value: string        // country code e.g. "CA"
    onChange: (code: string) => void
}

export function CountryPicker({ value, onChange }: Props) {
    const [open, setOpen] = useState(false)
    const [search, setSearch] = useState("")

    const selected = COUNTRIES.find(c => c.code === value) ?? COUNTRIES[0]
    const filtered = COUNTRIES.filter(c =>
        c.name.toLowerCase().includes(search.toLowerCase()) ||
        c.code.toLowerCase().includes(search.toLowerCase())
    )

    function pick(c: Country) {
        onChange(c.code)
        setOpen(false)
        setSearch("")
    }

    return (
        <>
            <TouchableOpacity style={styles.field} onPress={() => setOpen(true)} activeOpacity={0.75}>
                <Text style={styles.fieldFlag}>{selected.flag}</Text>
                <Text style={styles.fieldName}>{selected.name}</Text>
                <Text style={styles.fieldArrow}>▾</Text>
            </TouchableOpacity>

            <Modal visible={open} transparent animationType="slide" onRequestClose={() => setOpen(false)}>
                <Pressable style={styles.overlay} onPress={() => setOpen(false)} />
                <View style={styles.sheet}>
                    <View style={styles.handle} />
                    <Text style={styles.sheetTitle}>Select country</Text>

                    <TextInput
                        style={styles.search}
                        placeholder="Search…"
                        placeholderTextColor="#aaa"
                        value={search}
                        onChangeText={setSearch}
                        autoFocus
                    />

                    <FlatList
                        data={filtered}
                        keyExtractor={c => c.code}
                        renderItem={({ item }) => (
                            <TouchableOpacity
                                style={[styles.row, item.code === value && styles.rowActive]}
                                onPress={() => pick(item)}
                            >
                                <Text style={styles.rowFlag}>{item.flag}</Text>
                                <Text style={[styles.rowName, item.code === value && styles.rowNameActive]}>
                                    {item.name}
                                </Text>
                                {item.code === value && <Text style={styles.rowCheck}>✓</Text>}
                            </TouchableOpacity>
                        )}
                        ItemSeparatorComponent={() => <View style={styles.separator} />}
                        style={{ maxHeight: 320 }}
                    />
                </View>
            </Modal>
        </>
    )
}

const styles = StyleSheet.create({
    field: {
        flexDirection: "row", alignItems: "center",
        borderWidth: 1.5, borderColor: "#E0EDE0", borderRadius: 12,
        paddingHorizontal: 14, paddingVertical: 12,
        backgroundColor: "#FAFFFE", marginBottom: 14,
    },
    fieldFlag: { fontSize: 22, marginRight: 10 },
    fieldName: { flex: 1, fontSize: 15, color: "#1A3A1A" },
    fieldArrow: { color: "#888", fontSize: 13 },

    overlay: { flex: 1, backgroundColor: "rgba(0,0,0,0.4)" },
    sheet: {
        backgroundColor: "#fff", borderTopLeftRadius: 24,
        borderTopRightRadius: 24, padding: 20, paddingBottom: 32,
    },
    handle: {
        width: 40, height: 4, backgroundColor: "#D8EDD8",
        borderRadius: 2, alignSelf: "center", marginBottom: 16,
    },
    sheetTitle: { fontSize: 17, fontWeight: "700", color: "#1B5E20", marginBottom: 12 },
    search: {
        borderWidth: 1.5, borderColor: "#E0EDE0", borderRadius: 10,
        paddingHorizontal: 12, paddingVertical: 10,
        fontSize: 15, marginBottom: 12, color: "#1A3A1A",
    },
    row: {
        flexDirection: "row", alignItems: "center",
        paddingVertical: 12, paddingHorizontal: 4,
    },
    rowActive: { backgroundColor: "#F1F8F1", borderRadius: 8 },
    rowFlag: { fontSize: 22, marginRight: 12 },
    rowName: { flex: 1, fontSize: 15, color: "#333" },
    rowNameActive: { color: "#1B5E20", fontWeight: "600" },
    rowCheck: { color: "#2E7D32", fontWeight: "700" },
    separator: { height: 1, backgroundColor: "#F0F0F0" },
})
