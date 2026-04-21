import os
import io
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from domain.language import Language
from application.ports.i_stt_provider import ISTTProvider
from application.ports.i_tts_provider import ITTSProvider
from application.prompt_injection_guard import sanitise
from application.prompt_injection_guard import PromptInjectionDetectedError
from infrastructure.voice.whisper_stt_adapter import WhisperSTTAdapter
from infrastructure.voice.openai_tts_adapter import OpenAITTSAdapter
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def get_stt_provider() -> ISTTProvider:
    return WhisperSTTAdapter(client)

def get_tts_provider() -> ITTSProvider:
    return OpenAITTSAdapter(client)

@router.post("/voice/transcribe")
async def transcribe(file: UploadFile, stt: ISTTProvider = Depends(get_stt_provider)):
    if file.content_type not in ["audio/wav", "audio/mpeg", "audio/mp4", "audio/webm"]:
        raise HTTPException(status_code=415, detail="Unsupported audio format")
    
    audio_bytes = await file.read()

    if len(audio_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")
    
    try:
        transcript = stt.transcribe(audio_bytes)
        sanitise(transcript)
        return {"transcript": transcript}
    except PromptInjectionDetectedError:
        raise HTTPException(status_code=400, detail="Invalid input")
    
class SpeakRequest(BaseModel):
    text: str
    language: Language

@router.post("/voice/speak")
async def speak(request: SpeakRequest, tts: ITTSProvider = Depends(get_tts_provider)):
    audio_bytes = tts.synthesise(request.text, request.language)
    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")
