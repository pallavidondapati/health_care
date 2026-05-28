from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS
import uuid
import os
import io

router = APIRouter()

LANGUAGE_MAP = {
    "te": "te",
    "hi": "hi",
    "en": "en",
    "ta": "ta",
    "kn": "kn",
    "ml": "ml",
    "bn": "bn",
    "mr": "mr",
}

class TTSRequest(BaseModel):
    text: str
    language: str = "te"

@router.post("/text-to-speech")
async def text_to_speech(request: TTSRequest):

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")

    # Trim to 500 chars
    text = request.text[:500]
    lang = LANGUAGE_MAP.get(request.language, "en")

    temp_path = f"temp_tts_{uuid.uuid4().hex}.mp3"

    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(temp_path)

        # ✅ Read into memory and stream — no file left behind
        with open(temp_path, "rb") as f:
            audio_bytes = f.read()

        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=response.mp3"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)