import { useState, useRef } from "react"
import { Audio } from "expo-av"
import * as FileSystem from "expo-file-system"
import { API_BASE } from "../constants/api"

export function useVoice(sendMessage: (text: string) => Promise<string>, language: string) {
    const [isRecording, setIsRecording] = useState(false)
    const recordingRef = useRef<Audio.Recording | null>(null)

    async function startRecording() {
        await Audio.requestPermissionsAsync()
        await Audio.setAudioModeAsync({
            allowsRecordingIOS: true,
            playsInSilentModeIOS: true,
        })
        const { recording } = await Audio.Recording.createAsync(
            Audio.RecordingOptionsPresets.HIGH_QUALITY
        )
        recordingRef.current = recording
        setIsRecording(true)
    }

    async function stopRecording() {
        if (!recordingRef.current) return
        setIsRecording(false)

        await recordingRef.current.stopAndUnloadAsync()
        await Audio.setAudioModeAsync({ allowsRecordingIOS: false })

        const uri = recordingRef.current.getURI()
        recordingRef.current = null
        if (!uri) return

        const formData = new FormData()
        formData.append("file", { uri, name: "recording.m4a", type: "audio/m4a" } as any)

        const transcribeRes = await fetch(`${API_BASE}/voice/transcribe`, {
            method: "POST",
            body: formData,
        })
        const data = await transcribeRes.json()
        if (!data.transcript) return

        const responseText = await sendMessage(data.transcript)
        if (!responseText) return

        const ttsRes = await fetch(`${API_BASE}/voice/speak`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: responseText, language }),
        })
        const buffer = await ttsRes.arrayBuffer()
        const base64 = arrayBufferToBase64(buffer)
        const tempPath = `${FileSystem.cacheDirectory}tts_response.mp3`
        await FileSystem.writeAsStringAsync(tempPath, base64, {
            encoding: FileSystem.EncodingType.Base64,
        })
        const { sound } = await Audio.Sound.createAsync({ uri: tempPath })
        await sound.playAsync()
    }

    return { isRecording, startRecording, stopRecording }
}

function arrayBufferToBase64(buffer: ArrayBuffer): string {
    let binary = ""
    const bytes = new Uint8Array(buffer)
    for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i])
    }
    return btoa(binary)
}
