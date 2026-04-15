import { useState } from "react";
import * as ImagePicker from "expo-image-picker";
import * as ImageManipulator from "expo-image-manipulator";

export function useImagePicker() {
    const [imageUri, setImageUri] = useState<string | null>(null)
}