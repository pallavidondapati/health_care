from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# These should NEVER be emergency no matter what
NON_EMERGENCY_SYMPTOMS = [
    "sore throat", "throat pain", "cold", "runny nose",
    "mild headache", "body ache", "cough", "sneezing",
    "mild fever", "indigestion", "acidity", "bloating",
    "vomiting", "nausea", "stomach pain", "diarrhea",    # ← add these
    "stomach motion", "loose motion", "headache",         # ← add these
    "fever", "body pain", "weakness", "fatigue",          # ← add these
    "తలనొప్పి", "జలుబు", "దగ్గు", "వాంతులు",
    "सर्दी", "खांसी", "गले में दर्द", "उल्टी",
]

EMERGENCY_RULES = [
    # English
    "chest pain", "cannot breathe", "can't breathe", "not breathing",
    "unconscious", "unresponsive", "heart attack", "cardiac arrest",
    "severe bleeding", "stroke", "face drooping", "arm weakness",
    "poisoning", "overdose", "seizure", "convulsion",
    # Telugu
    "ఛాతీ నొప్పి", "శ్వాస రావడం లేదు", "స్పృహ కోల్పోయాడు",
    "గుండె పోటు", "రక్తస్రావం", "మూర్ఛ",
    # Hindi
    "सीने में दर्द", "सांस नहीं आ रही", "बेहोश",
    "दिल का दौरा", "खून बह रहा है", "दौरा",
    # Tamil
    "மார்பு வலி", "மூச்சு வரவில்லை", "இதய அடைப்பு",
    # Kannada
    "ಎದೆ ನೋವು", "ಉಸಿರಾಟ ಇಲ್ಲ", "ಪ್ರಜ್ಞೆ ತಪ್ಪಿದೆ",
]

HIGH_RISK_RULES = [
    "difficulty breathing", "breathlessness", "high fever",
    "severe vomiting", "blood in urine", "blood in stool",
    "severe headache", "sudden vision loss", "sudden numbness",
    "నిమోనియా", "అధిక జ్వరం", "రక్తం వస్తోంది",
    "तेज बुखार", "खून आ रहा है",
]

BLOCKED_RESPONSES = [
    "take aspirin", "take paracetamol", "take ibuprofen",
    "you have diabetes", "you have cancer", "you have covid",
    "you are diagnosed", "prescribed", "dosage",
]

class SafetyRequest(BaseModel):
    transcript: str
    symptoms: list[str]
    severity: str
    ai_response: str | None = None

class SafetyResponse(BaseModel):
    is_safe: bool
    severity: str
    override_reason: str | None
    filtered_response: str | None
    call_108: bool

@router.post("/safety-check", response_model=SafetyResponse)
async def safety_check(request: SafetyRequest):

    transcript_lower = request.transcript.lower()
    symptoms_text = " ".join(request.symptoms).lower()
    combined = transcript_lower + " " + symptoms_text

    # ✅ Rule 0 — Non-emergency downgrade FIRST
    # Sore throat, cold, cough etc should NEVER be emergency
    for safe_symptom in NON_EMERGENCY_SYMPTOMS:
        if safe_symptom.lower() in combined:
            if request.severity == "emergency":
                return SafetyResponse(
                    is_safe=False,
                    severity="moderate",
                    override_reason=f"Non-emergency symptom '{safe_symptom}' — downgraded from emergency",
                    filtered_response=None,
                    call_108=False
                )

    # Rule 1 — Emergency keyword override
    for keyword in EMERGENCY_RULES:
        if keyword.lower() in combined:
            return SafetyResponse(
                is_safe=False,
                severity="emergency",
                override_reason=f"Emergency keyword detected: '{keyword}'",
                filtered_response="🚨 This is a medical emergency! Please call 108 immediately or go to the nearest hospital now. Do not wait.",
                call_108=True
            )

    # Rule 2 — High risk symptom escalation
    if request.severity == "low":
        for keyword in HIGH_RISK_RULES:
            if keyword.lower() in combined:
                return SafetyResponse(
                    is_safe=False,
                    severity="moderate",
                    override_reason=f"High risk symptom detected: '{keyword}' — escalating from low to moderate",
                    filtered_response="Your symptoms need medical attention. Please visit a nearby clinic or PHC today.",
                    call_108=False
                )

    # Rule 3 — Filter unsafe AI responses
    filtered_response = request.ai_response
    if request.ai_response:
        response_lower = request.ai_response.lower()
        for blocked in BLOCKED_RESPONSES:
            if blocked.lower() in response_lower:
                filtered_response = "Please consult a qualified doctor for proper medical advice. Do not self-medicate."
                return SafetyResponse(
                    is_safe=False,
                    severity=request.severity,
                    override_reason=f"Unsafe medical advice detected: '{blocked}'",
                    filtered_response=filtered_response,
                    call_108=False
                )

    # All checks passed
    return SafetyResponse(
        is_safe=True,
        severity=request.severity,
        override_reason=None,
        filtered_response=request.ai_response,
        call_108=request.severity == "emergency"
    )