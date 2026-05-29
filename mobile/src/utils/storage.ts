import { Platform } from "react-native"
import * as SecureStore from "expo-secure-store"
import AsyncStorage from "@react-native-async-storage/async-storage"

// expo-secure-store is native-only. On web we fall back to AsyncStorage.
// Tokens stored via AsyncStorage on web are less secure (localStorage-backed)
// but acceptable for development. Native builds always use the OS keychain.

export async function getSecureItem(key: string): Promise<string | null> {
    if (Platform.OS === "web") return AsyncStorage.getItem(key)
    return SecureStore.getItemAsync(key)
}

export async function setSecureItem(key: string, value: string): Promise<void> {
    if (Platform.OS === "web") { await AsyncStorage.setItem(key, value); return }
    await SecureStore.setItemAsync(key, value)
}

export async function deleteSecureItem(key: string): Promise<void> {
    if (Platform.OS === "web") { await AsyncStorage.removeItem(key); return }
    await SecureStore.deleteItemAsync(key)
}
