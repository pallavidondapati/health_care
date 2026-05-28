from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

router = APIRouter()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "triage_model")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)

# Load model once at startup
print("Loading triage model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()
print("Triage model loaded!")

LABELS = {0: "low", 1: "moderate", 2: "high", 3: "emergency"}

ADVICE = {
    "low": "Your symptoms appear mild. Rest well, drink plenty of fluids, and monitor your condition.",
    "moderate": "Your symptoms need attention. Please visit a nearby clinic or PHC within 24 hours.",
    "high": "Your symptoms are serious. Please visit a hospital urgently today.",
    "emergency": "This is a medical emergency! Call 108 immediately or go to the nearest emergency room now."
}

class TriageRequest(BaseModel):
    symptoms: list[str]
    duration: str | None = None
    severity_hint: str | None = None
    is_emergency: bool = False

@router.post("/triage")
async def triage(request: TriageRequest):

    if not request.symptoms:
        raise HTTPException(status_code=400, detail="No symptoms provided")

    # Force emergency if flagged by symptom extractor
    if request.is_emergency:
        return {
            "severity": "emergency",
            "advice": ADVICE["emergency"],
            "confidence": 1.0,
            "call_108": True
        }

    # Build input text from symptoms
    input_text = ", ".join(request.symptoms)
    if request.duration:
        input_text += f" for {request.duration}"

    # Tokenize and predict
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probs, dim=-1).item()
        confidence = probs[0][predicted_class].item()

    severity = LABELS[predicted_class]

    # Override with severity_hint if model confidence is low
    if confidence < 0.6 and request.severity_hint:
        hint_map = {"mild": "low", "moderate": "moderate", "severe": "high"}
        severity = hint_map.get(request.severity_hint, severity)

    return {
        "severity": severity,
        "advice": ADVICE[severity],
        "confidence": round(confidence, 2),
        "call_108": severity == "emergency"
    }
