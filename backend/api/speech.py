from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import os
import uuid
import subprocess
import numpy as np
import unicodedata
from groq import Groq
from dotenv import load_dotenv
from itertools import groupby

load_dotenv()

router = APIRouter()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SUPPORTED_LANGUAGES = {"te", "hi", "en", "ta", "kn", "ml", "bn", "mr"}

def convert_to_wav(input_path: str) -> str:
    output_path = input_path.rsplit(".", 1)[0] + ".wav"
    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        output_path,
        "-y",
        "-loglevel", "error"
    ], check=True)
    return output_path

def detect_script(text: str) -> str:
    for char in text:
        name = unicodedata.name(char, "")
        if "TELUGU" in name:
            return "te"
        if "TAMIL" in name:
            return "ta"
        if "DEVANAGARI" in name:
            return "hi"
        if "KANNADA" in name:
            return "kn"
        if "MALAYALAM" in name:
            return "ml"
        if "BENGALI" in name:
            return "bn"
    return "en"

def is_looping(text: str, threshold: int = 3) -> bool:
    words = text.strip().split()
    if len(words) < 6:
        return False
    groups = [(k, len(list(v))) for k, v in groupby(words)]
    return any(count >= threshold for _, count in groups)

@router.post('/transcribe')
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = Form("te")  # ✅ accept language from frontend
):
    temp_path = f"temp_{uuid.uuid4().hex}_{audio.filename}"
    wav_path = None

    try:
        with open(temp_path, "wb") as buffer:
            buffer.write(await audio.read())

        wav_path = convert_to_wav(temp_path)

        # Silence check
        try:
            import whisper as _whisper
            audio_array = _whisper.load_audio(wav_path)
            if len(audio_array) < 16000 * 0.5:
                raise HTTPException(status_code=400, detail="Audio too short")
            rms = np.sqrt(np.mean(audio_array**2))
            if rms < 0.001:
                raise HTTPException(status_code=400, detail="Audio is silent or too quiet")
        except ImportError:
            pass

        # ✅ Pass language hint to Groq — fixes Telugu/Tamil confusion
        with open(wav_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=("audio.wav", audio_file, "audio/wav"),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
                language=language,  # ✅ tell Groq what language to expect
            )

        transcript = transcription.text.strip()

        # Trust script detection over Groq
        script_lang = detect_script(transcript)
        detected_lang = script_lang if script_lang != "en" else language

        if not transcript:
            return {"transcript": "", "language": detected_lang, "warning": "No speech detected"}

        if is_looping(transcript):
            return {"transcript": "", "language": detected_lang, "warning": "Could not understand audio clearly"}

        return {
            "transcript": transcript,
            "language": detected_lang,
            "confidence": 0.95
        }

    except subprocess.CalledProcessError:
        raise HTTPException(status_code=400, detail="Audio conversion failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)