import anthropic
import base64
import os

class ClaudeImageAnalyzer:

    def __init__(self, api_key: str):
        self._api_key = api_key

    def analyse_image(self, image_url: str) -> str:
        filename = image_url.split("/uploads/")[-1]
        file_path = os.path.join("uploads", filename)
        ext = filename.rsplit(".", 1)[-1].lower()
        media_type = "image/png" if ext == "png" else "image/webp" if ext == "webp" else "image/jpeg"

        with open(file_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        client = anthropic.Anthropic(api_key=self._api_key)
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}},
                {"type": "text", "text": "Analyse this crop image. Identify any visible diseases, pests, or nutrient deficiencies. Be specific and concise."}
            ]}]
        )
        return response.content[0].text
    