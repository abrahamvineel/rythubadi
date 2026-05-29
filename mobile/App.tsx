/**
 * App.tsx — thin shell.
 *
 * Responsibilities:
 *   1. Auth guard       — Login / Register while no token
 *   2. Onboarding       — OnboardingScreen until AsyncStorage flag is set
 *   3. Responsive shell — left NavSidebar on desktop (≥768px), bottom TabBar on mobile
 *   4. Cross-tab nav    — Feed "View <entity>" switches to Monitor + deep-links
 *   5. ProfileSheet     — global overlay with logout, opened by any screen or sidebar
 *   6. Logout           — wired into NavSidebar (desktop) and ProfileSheet (all sizes)
 */
import React, { useState, useEffect } from "react"
import AsyncStorage from "@react-native-async-storage/async-storage"
import { SafeAreaProvider } from "react-native-safe-area-context"
import { View, StyleSheet, useWindowDimensions, Alert } from "react-native"

import { useAuth } from "./src/hooks/useAuth"
import { decodeToken } from "./src/utils/token"
import { useFeed } from "./src/hooks/useFeed"

import { LoginScreen } from "./src/screens/LoginScreen"
import { RegisterScreen } from "./src/screens/RegisterScreen"
import { OnboardingScreen } from "./src/screens/OnboardingScreen"
import { FeedScreen } from "./src/screens/FeedScreen"
import { MonitorScreen, MonitorTarget } from "./src/screens/MonitorScreen"
import { ChatsScreen } from "./src/screens/ChatsScreen"
import { TabBar, Tab } from "./src/components/TabBar"
import { NavSidebar } from "./src/components/NavSidebar"
import { ProfileSheet } from "./src/components/ProfileSheet"
import { FeedEvent } from "./src/types/feed"

// Screen width at which the layout switches from bottom tabs to a left sidebar.
const DESKTOP_BREAKPOINT = 768

// ─── Main authenticated shell ──────────────────────────────────────────────────

function MainApp({
    token,
    language,
    provinceState,
    country,
    logout,
}: {
    token: string
    language: string
    provinceState: string
    country: string
    logout: () => void
}) {
    const { width } = useWindowDimensions()
    const isDesktop = width >= DESKTOP_BREAKPOINT

    const [activeTab, setActiveTab] = useState<Tab>("feed")
    const [profileOpen, setProfileOpen] = useState(false)
    const [monitorTarget, setMonitorTarget] = useState<MonitorTarget | null>(null)
    const { unreadAlerts } = useFeed(token)

    /**
     * handleViewSubject — called when the farmer taps "View <entity>" on a feed card.
     * Switches to Monitor tab and passes a deep-link target so MonitorScreen navigates
     * straight to the right entity (animal, location, zone, etc.).
     *
     * This is the single routing function for cross-tab navigation.
     * Adding a new subject type: no change here — MonitorScreen handles unknown types
     * gracefully by staying on overview.
     */
    function handleViewSubject(event: FeedEvent) {
        if (!event.subject_type || !event.subject_id) return
        setMonitorTarget({
            subjectType: event.subject_type,
            subjectId: event.subject_id,
            locationId: event.location_id,
        })
        setActiveTab("monitor")
    }

    /**
     * handleTabSelect — clear the deep-link target when the farmer manually taps
     * Monitor in the nav. They want the overview, not the last feed card's entity.
     */
    function handleTabSelect(tab: Tab) {
        if (tab === "monitor") setMonitorTarget(null)
        setActiveTab(tab)
    }

    function confirmLogout() {
        Alert.alert(
            "Log out?",
            "You'll need to sign in again to access your farm data.",
            [
                { text: "Cancel", style: "cancel" },
                { text: "Log out", style: "destructive", onPress: logout },
            ],
        )
    }

    // ── Screens — same on both layouts ───────────────────────────────────────

    const screens = (
        <>
            {activeTab === "feed" && (
                <FeedScreen
                    token={token}
                    language={language}
                    country={country}
                    onOpenProfile={() => setProfileOpen(true)}
                    onViewSubject={handleViewSubject}
                />
            )}
            {activeTab === "monitor" && (
                <MonitorScreen token={token} target={monitorTarget} />
            )}
            {activeTab === "chats" && (
                <ChatsScreen
                    token={token}
                    language={language}
                    provinceState={provinceState}
                    country={country}
                    onOpenProfile={() => setProfileOpen(true)}
                />
            )}
        </>
    )

    // ── Desktop layout — left sidebar + content ───────────────────────────────

    if (isDesktop) {
        return (
            <View style={styles.desktopRoot}>
                <NavSidebar
                    active={activeTab}
                    onSelect={handleTabSelect}
                    alertCount={unreadAlerts}
                    onOpenProfile={() => setProfileOpen(true)}
                    onLogout={confirmLogout}
                />
                <View style={styles.desktopContent}>
                    {screens}
                </View>
                <ProfileSheet
                    visible={profileOpen}
                    token={token}
                    onClose={() => setProfileOpen(false)}
                    onLogout={logout}
                />
            </View>
        )
    }

    // ── Mobile layout — content + bottom tab bar ──────────────────────────────

    return (
        <View style={styles.mobileRoot}>
            {screens}
            <TabBar
                active={activeTab}
                onSelect={handleTabSelect}
                alertCount={unreadAlerts}
            />
            <ProfileSheet
                visible={profileOpen}
                token={token}
                onClose={() => setProfileOpen(false)}
                onLogout={logout}
            />
        </View>
    )
}

// ─── Auth + onboarding guard ───────────────────────────────────────────────────

function AppContent() {
    const {
        token,
        language,
        provinceState,
        country,
        loading: authLoading,
        error: authError,
        login,
        register,
        logout,
    } = useAuth()

    const [authScreen, setAuthScreen] = useState<"login" | "register">("login")
    const [onboardingDone, setOnboardingDone] = useState<boolean | null>(null)

    useEffect(() => {
        if (!token) { setOnboardingDone(null); return }
        const decoded = decodeToken(token)
        const userId = decoded?.user_id
        if (!userId) { setOnboardingDone(true); return }
        AsyncStorage.getItem(`onboarding_done_${userId}`)
            .then(val => setOnboardingDone(val === "true"))
            .catch(() => setOnboardingDone(true))
    }, [token])

    async function handleOnboardingComplete() {
        const decoded = decodeToken(token!)
        const userId = decoded?.user_id
        if (userId) await AsyncStorage.setItem(`onboarding_done_${userId}`, "true")
        setOnboardingDone(true)
    }

    if (authLoading) return null
    if (token && onboardingDone === null) return null

    if (!token) {
        if (authScreen === "register")
            return <RegisterScreen onRegister={register} onGoToLogin={() => setAuthScreen("login")} error={authError} />
        return <LoginScreen onLogin={login} onGoToRegister={() => setAuthScreen("register")} error={authError} />
    }

    if (!onboardingDone)
        return <OnboardingScreen token={token} onComplete={handleOnboardingComplete} />

    return (
        <MainApp
            token={token}
            language={language ?? "EN"}
            provinceState={provinceState ?? "general"}
            country={country ?? "CA"}
            logout={logout}
        />
    )
}

// ─── Root ──────────────────────────────────────────────────────────────────────

export default function App() {
    return (
        <SafeAreaProvider>
            <AppContent />
        </SafeAreaProvider>
    )
}

const styles = StyleSheet.create({
    // Desktop: sidebar on the left, content fills the rest
    desktopRoot: {
        flex: 1,
        flexDirection: "row",
        backgroundColor: "#F4F9F4",
    },
    desktopContent: {
        flex: 1,
        // Constrain chat/feed content so it doesn't stretch to 1500px on wide monitors.
        // The sidebar already takes 220px — this keeps the content readable.
        maxWidth: 900,
    },

    // Mobile: screens stack with TabBar pinned at the bottom
    mobileRoot: {
        flex: 1,
        backgroundColor: "#F4F9F4",
    },
})
