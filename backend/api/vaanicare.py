from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from backend.api.speech import transcribe_audio
from backend.api.symptom import extract_symptoms, TranscriptRequest
from backend.api.triage import triage, TriageRequest
from backend.api.safety import safety_check, SafetyRequest
from backend.api.response import generate_response, ResponseRequest, Message
from backend.api.facility import nearest_facility, LocationRequest
import traceback
import json

router = APIRouter()

BP_TERMS = ["bp", "బీపీ", "blood pressure", "బ్లడ్ ప్రెషర్", "రక్తపోటు"]
DIABETES_TERMS = ["sugar", "షుగర్", "diabetes", "మధుమేహం", "diabetic"]

@router.post("/vaanicare")
async def vaanicare_pipeline(
    audio: UploadFile = File(...),
    latitude: float = 18.1066,
    longitude: float = 83.3956,
    language: str = "te",
    history: str = Form("[]"),
    symptoms: str = Form("[]"),
):
    result = {}

    try:
        # Parse history and accumulated symptoms
        conversation_history = [Message(**m) for m in json.loads(history)]
        accumulated_symptoms = json.loads(symptoms)

        # ─── STEP 1: Speech to Text ───────────────────────────
        print("Step 1: Transcribing audio...")
        stt_result = await transcribe_audio(audio=audio, language=language)
        transcript = stt_result["transcript"]
        language = stt_result["language"]
        confidence = stt_result.get("confidence", 0)

        if not transcript:
            raise HTTPException(status_code=400, detail="Could not understand audio, please try again")

        result["transcript"] = transcript
        result["language"] = language
        result["stt_confidence"] = confidence
        print(f"  → Transcript: {transcript}")

        # ─── STEP 2: Symptom Extraction ───────────────────────
        print("Step 2: Extracting symptoms...")
        symptom_result = await extract_symptoms(
            TranscriptRequest(transcript=transcript, language=language)
        )
        new_symptoms = symptom_result.get("symptoms", [])
        duration = symptom_result.get("duration")
        severity_hint = symptom_result.get("severity_hint")
        is_emergency = symptom_result.get("is_emergency", False)

        current_text = transcript.lower()

        # ✅ Smart symptom merging
        if new_symptoms:
            all_symptoms = list(set(accumulated_symptoms + new_symptoms))
        else:
            all_symptoms = accumulated_symptoms

        # ✅ BP override — clear unrelated symptoms
        if any(term in current_text for term in BP_TERMS):
            all_symptoms = [s for s in all_symptoms if any(
                bp in s.lower() for bp in [
                    "blood pressure", "hypertension", "bp",
                    "headache", "dizziness", "blurred vision"
                ]
            )]
            if "high blood pressure" not in all_symptoms:
                all_symptoms.insert(0, "high blood pressure")

        # ✅ Diabetes override — clear unrelated symptoms
        if any(term in current_text for term in DIABETES_TERMS):
            all_symptoms = [s for s in all_symptoms if any(
                d in s.lower() for d in [
                    "diabetes", "blood sugar", "thirst",
                    "urination", "fatigue", "weight loss"
                ]
            )]
            if "diabetes symptoms" not in all_symptoms:
                all_symptoms.insert(0, "diabetes symptoms")

        result["symptoms"] = all_symptoms
        result["duration"] = duration
        print(f"  → Symptoms: {all_symptoms}")

        # ─── STEP 3: Triage ───────────────────────────────────
        print("Step 3: Running triage...")
        if all_symptoms:
            triage_result = await triage(
                TriageRequest(
                    symptoms=all_symptoms,
                    duration=duration,
                    severity_hint=severity_hint,
                    is_emergency=is_emergency
                )
            )
            severity = triage_result["severity"]
            triage_confidence = triage_result["confidence"]
        else:
            severity = "low"
            triage_confidence = 0

        result["severity"] = severity
        result["triage_confidence"] = triage_confidence
        print(f"  → Severity: {severity}")

        # ─── STEP 4: Safety Check ─────────────────────────────
        print("Step 4: Running safety check...")
        safety_result = await safety_check(
            SafetyRequest(
                transcript=transcript,
                symptoms=all_symptoms,
                severity=severity,
                ai_response=None
            )
        )
        if not safety_result.is_safe:
            severity = safety_result.severity
            result["severity"] = severity
            result["safety_override"] = safety_result.override_reason
        print(f"  → Safety passed: {safety_result.is_safe}")

        # ─── STEP 5: RAG Response with History ────────────────
        print("Step 5: Generating response...")
        response_result = await generate_response(
            ResponseRequest(
                transcript=transcript,
                symptoms=all_symptoms if all_symptoms else ["general health query"],
                severity=severity,
                language=language,
                history=conversation_history
            )
        )
        ai_response = response_result["response"]

        # ─── STEP 6: Final Safety Filter ──────────────────────
        final_safety = await safety_check(
            SafetyRequest(
                transcript=transcript,
                symptoms=all_symptoms,
                severity=severity,
                ai_response=ai_response
            )
        )
        final_response = final_safety.filtered_response or ai_response
        result["response"] = final_response
        result["call_108"] = final_safety.call_108
        print("  → Response generated")

        # ─── STEP 7: Facilities ───────────────────────────────
        try:
            print("Step 7: Finding nearest facilities...")
            facility_result = await nearest_facility(
                LocationRequest(
                    latitude=latitude,
                    longitude=longitude,
                    severity=severity
                )
            )
            result["facilities"] = facility_result.get("facilities", [])[:3]
            print(f"  → Found {len(result['facilities'])} facilities")
        except Exception:
            result["facilities"] = []
            print("  → Facility search failed, continuing...")

        # ✅ Update conversation history
        updated_history = conversation_history + [
            Message(role="user", content=transcript),
            Message(role="assistant", content=final_response)
        ]

        # ─── FINAL RESPONSE ───────────────────────────────────
        return {
            "success": True,
            "transcript": result["transcript"],
            "language": result["language"],
            "symptoms": result["symptoms"],
            "duration": result.get("duration"),
            "severity": result["severity"],
            "response": result["response"],
            "call_108": result["call_108"],
            "facilities": result["facilities"],
            "history": [m.dict() for m in updated_history],
            "accumulated_symptoms": all_symptoms,
            "debug": {
                "stt_confidence": result["stt_confidence"],
                "triage_confidence": result["triage_confidence"],
                "safety_override": result.get("safety_override")
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")