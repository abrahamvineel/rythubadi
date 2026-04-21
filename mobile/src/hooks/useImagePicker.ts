import { useState } from "react";
import * as ImagePicker from "expo-image-picker";
import * as ImageManipulator from "expo-image-manipulator";

export function useImagePicker() {
    const [imageUri, setImageUri] = useState<string | null>(null)

    async function pickImage() {
        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            quality: 0.8
        })

        if (result.canceled) return

        const stripped = await ImageManipulator.manipulateAsync(
            result.assets[0].uri,
            [],
            { format: ImageManipulator.SaveFormat.JPEG }
        )

        setImageUri(stripped.uri)
    }
    
    async function uploadImage(): Promise<string | null> {
        if (!imageUri) return null

        const formData = new FormData()

        if (imageUri.startsWith("blob:") || imageUri.startsWith("data:")) {
            const response = await fetch(imageUri)
            const blob = await response.blob()
            const file = new File([blob], "photo.jpg", { type: "image/jpeg" })
            formData.append("file", file, "photo.jpg")
        } else {
            formData.append("file", { uri: imageUri, name: "photo.jpg", type: "image/jpeg" } as any)
        }

        const res = await fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData,
        })

        if (!res.ok) return null
        const data = await res.json()
        return data.url
    }

    function clearImage() {
        setImageUri(null)
    }
    return { imageUri, pickImage, uploadImage, clearImage }
}