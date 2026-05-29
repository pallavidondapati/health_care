from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

LABELS = {0: "low", 1: "moderate", 2: "high", 3: "emergency"}

ADVICE = {
    "low": "Your symptoms appear mild. Rest well, drink plenty of fluids, and monitor your condition.",
    "moderate": "Your symptoms need attention. Please visit a nearby clinic or PHC within 24 hours.",
    "high": "Your symptoms are serious. Please visit a hospital urgently today.",
    "emergency": "This is a medical emergency! Call 108 immediately or go to the nearest emergency room now."
}

# ✅ Safe import — won't crash on Render without torch
tokenizer = None
model = None

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.path.join(BASE_DIR, "ml", "triage_model")
    if os.path.exists(MODEL_PATH):
        print("Loading triage model...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        model.eval()
        print("Triage model loaded!")
    else:
        print("⚠️ Triage model not found — using rule-based fallback")
except Exception as e:
    print(f"⚠️ Triage model not available: {e} — using rule-based fallback")


def rule_based_triage(symptoms: list, severity_hint: str = None) -> tuple:
    """Rule-based fallback when ML model not available"""
    symptoms_text = " ".join(symptoms).lower()

    emergency_keywords = [
        "chest pain", "cannot breathe", "unconscious",
        "heart attack", "stroke", "severe bleeding", "convulsion", "seizure"
    ]
    high_keywords = [
        "difficulty breathing", "breathlessness", "high fever",
        "blood in stool", "blood in urine", "severe headache", "sudden numbness"
    ]
    moderate_keywords = [
        "fever", "vomiting", "diarrhea", "stomach pain", "loose motions",
        "headache", "body pain", "cough", "sore throat", "nausea",
        "high blood pressure", "diabetes", "weakness", "fatigue",
        "acidity", "indigestion", "cold", "runny nose"
    ]

    if any(k in symptoms_text for k in emergency_keywords):
        return "emergency", 0.95
    if any(k in symptoms_text for k in high_keywords):
        return "high", 0.85
    if any(k in symptoms_text for k in moderate_keywords):
        return "moderate", 0.75

    if severity_hint:
        hint_map = {"mild": "low", "moderate": "moderate", "severe": "high"}
        return hint_map.get(severity_hint, "low"), 0.60

    return "low", 0.50


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

    # ✅ Use ML model if available, else rule-based fallback
    if model is not None and tokenizer is not None:
        try:
            import torch
            input_text = ", ".join(request.symptoms)
            if request.duration:
                input_text += f" for {request.duration}"

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

            # Override with hint if confidence is low
            if confidence < 0.6 and request.severity_hint:
                hint_map = {"mild": "low", "moderate": "moderate", "severe": "high"}
                severity = hint_map.get(request.severity_hint, severity)

        except Exception as e:
            print(f"Model inference failed: {e} — using fallback")
            severity, confidence = rule_based_triage(
                request.symptoms, request.severity_hint
            )
    else:
        severity, confidence = rule_based_triage(
            request.symptoms, request.severity_hint
        )

    return {
        "severity": severity,
        "advice": ADVICE[severity],
        "confidence": round(confidence, 2),
        "call_108": severity == "emergency"
    }
