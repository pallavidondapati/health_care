from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

router = APIRouter()

# ----------------------------
# MODEL PATH (Render-safe)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "triage_model")

tokenizer = None
model = None

# ----------------------------
# LABELS + ADVICE
# ----------------------------
LABELS = {
    0: "low",
    1: "moderate",
    2: "high",
    3: "emergency"
}

ADVICE = {
    "low": "Your symptoms appear mild. Rest well, drink fluids, and monitor your condition.",
    "moderate": "Please visit a nearby clinic or PHC within 24 hours.",
    "high": "Your symptoms are serious. Visit a hospital urgently today.",
    "emergency": "Medical emergency! Call 108 immediately or go to ER now."
}

# ----------------------------
# REQUEST MODEL
# ----------------------------
class TriageRequest(BaseModel):
    symptoms: list[str]
    duration: str | None = None
    severity_hint: str | None = None
    is_emergency: bool = False


# ----------------------------
# LOAD MODEL ON STARTUP
# ----------------------------
@router.on_event("startup")
def load_model():
    global tokenizer, model

    print("Loading triage model...")

    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model folder not found: {MODEL_PATH}")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        local_files_only=True
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_PATH
    )

    model.eval()

    print("Triage model loaded successfully!")


# ----------------------------
# PREDICTION ENDPOINT
# ----------------------------
@router.post("/triage")
async def triage(request: TriageRequest):

    if not request.symptoms:
        raise HTTPException(status_code=400, detail="No symptoms provided")

    # Emergency override
    if request.is_emergency:
        return {
            "severity": "emergency",
            "advice": ADVICE["emergency"],
            "confidence": 1.0,
            "call_108": True
        }

    # Build input text
    input_text = ", ".join(request.symptoms)

    if request.duration:
        input_text += f" for {request.duration}"

    # Tokenize
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    )

    # Predict
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)

        predicted_class = torch.argmax(probs, dim=-1).item()
        confidence = probs[0, predicted_class].item()

    severity = LABELS[predicted_class]

    # Override if low confidence + hint
    if confidence < 0.6 and request.severity_hint:
        hint_map = {
            "mild": "low",
            "moderate": "moderate",
            "severe": "high"
        }
        severity = hint_map.get(request.severity_hint, severity)

    return {
        "severity": severity,
        "advice": ADVICE[severity],
        "confidence": round(confidence, 2),
        "call_108": severity == "emergency"
    }
