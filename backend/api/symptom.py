from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os
import time

load_dotenv()

router = APIRouter()

PROMPT_TEMPLATE = """
You are a medical symptom extractor for rural India.

STRICT RULES:
- Extract ONLY symptoms explicitly mentioned in THIS transcript
- Do NOT add extra symptoms that are not clearly stated
- Do NOT assume related symptoms
- If patient says "BP" or "blood pressure" → extract ONLY "high blood pressure"
- If patient says "sugar" → extract ONLY "diabetes symptoms"  
- If patient says "fever" → extract ONLY "fever"
- Do NOT extract symptoms from greetings or questions

Common rural Indian terms:
- "BP" or "బీపీ" = high blood pressure
- "sugar" or "షుగర్" = diabetes
- "motions" or "loose motions" = diarrhea
- "jaram/jwaram/జారం" = fever
- "head pain/తలనొప్పి" = headache
- "stomach upset" = nausea

Return ONLY this JSON:
{{
  "symptoms": ["ONLY symptoms clearly mentioned"],
  "duration": "duration if mentioned or null",
  "body_part": "affected body part or null",
  "severity_hint": "mild | moderate | severe | null",
  "is_emergency": true or false,
  "original_language": "te/hi/en/ta/kn"
}}

THIS transcript only — ignore conversation history:
Transcript: {transcript}
"""
EMERGENCY_KEYWORDS = [
    "chest pain", "can't breathe", "cannot breathe",
    "unconscious", "stroke", "heart attack", "severe bleeding"
]

class TranscriptRequest(BaseModel):
    transcript: str
    language: str = "te"

def get_chain():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    prompt = PromptTemplate(
        input_variables=["transcript"],
        template=PROMPT_TEMPLATE
    )
    parser = JsonOutputParser()
    return prompt | llm | parser

@router.post("/extract-symptoms")
async def extract_symptoms(request: TranscriptRequest):

    if not request.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript is empty")

    for attempt in range(3):
        try:
            chain = get_chain()
            extracted = await chain.ainvoke({"transcript": request.transcript})

            # Force emergency override regardless of model output
            if any(kw in request.transcript.lower() for kw in EMERGENCY_KEYWORDS):
                extracted["is_emergency"] = True

            return extracted

        except Exception as e:
            if "429" in str(e) and attempt < 2:
                time.sleep(10)  # Groq rate limit is shorter than Gemini
                continue
            raise HTTPException(status_code=500, detail=f"LangChain error: {str(e)}")