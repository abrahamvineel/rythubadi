import { useState, useRef} from "react"

export function useVoice(sendMessage: (text: string) => Promise<void>) {
    const [isRecording, setIsRecording] = useState(false)

    const mediaRecorderRef = useRef<MediaRecorder | null>(null)

    const chunksRef = useRef<Blob[]>([])

    async function startRecording() {
        const stream = await navigator.mediaDevices.getUserMedia({audio: true})

        chunksRef.current = []

        const recorder = new MediaRecorder(stream)
        recorder.ondataavailable = (e) => chunksRef.current.push(e.data)

        mediaRecorderRef.current = recorder
        recorder.start()
        setIsRecording(true)
    }

    function stopRecording() {
        if (!mediaRecorderRef.current) return

        mediaRecorderRef.current.onstop = async () => {
            const audioBlob = new Blob(chunksRef.current, { type: "audio/webm" })
            const formData = new FormData()
            formData.append("file", audioBlob, "recording.webm")

            const res = await fetch("http://localhost:8000/voice/transcribe", {
                method: "POST",
                body: formData,
            })
            const data = await res.json()
            await sendMessage(data.transcript)
        }
        mediaRecorderRef.current.stop()
        setIsRecording(false)
    }
    return { isRecording, startRecording, stopRecording }
}
