import React from "react";
import { TouchableOpacity, Text, StyleSheet } from "react-native";

type Props = {
    isRecording: boolean
    onStart: () => void
    onStop: () => void
}

export function VoiceButton({ isRecording, onStart, onStop}: Props) {
    return (
        <TouchableOpacity
            style={isRecording ? styles.recording : styles.idle}
            onPress={isRecording ? onStop : onStart}
        >
            <Text style={styles.label}>
                {isRecording ? "🔴" : "🎤"}
            </Text>
        </TouchableOpacity>
    )
}

const styles = StyleSheet.create({
    idle: {
        backgroundColor: "#4CAF50",
        width: 44,
        height: 44,
        borderRadius: 22,
        alignItems: "center",
        justifyContent: "center",
    },
    recording: {
        backgroundColor: "#F44336",
        width: 44,
        height: 44,
        borderRadius: 22,
        alignItems: "center",
        justifyContent: "center",
    },
    label: {
        fontSize: 20,
    },
})