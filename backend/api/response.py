from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from backend.ml.rag import retrieve_context
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

SYSTEM_PROMPT = """
You are VaaniCare, a safe and knowledgeable AI healthcare assistant for rural India.
You are like a trusted community doctor who speaks the patient's language.

MEDICAL KNOWLEDGE:
{context}

CURRENT SYMPTOMS: {symptoms}
SEVERITY: {severity}

RESPONSE RULES based on severity:

If severity is "low":
1. Start with empathy — acknowledge their concern warmly
2. Explain WHY this symptom occurs (1-2 simple sentences)
3. Give 2-3 specific home remedies from medical knowledge
4. Mention common OTC medicine if relevant (Paracetamol/Dolo 650 for fever/pain) with note to consult pharmacist
5. Say clearly what NOT to do
6. Say when to visit doctor if not better

If severity is "moderate":
1. Start with empathy
2. Briefly explain why this occurs
3. Give 1-2 safe home remedies from medical knowledge
4. Mention OTC medicine if safe and relevant, with pharmacist consultation note
5. Clearly say "visit PHC or clinic within 24 hours"
6. Mention warning signs to watch for

If severity is "high":
1. Be urgent but calm
2. Say "please visit hospital today — do not delay"
3. NO home remedies
4. List danger signs to watch for immediately

If severity is "emergency":
1. Say "Call 108 immediately" — nothing else matters
2. One line of what to do while waiting
3. No home remedies

IMPORTANT RULES:
- Respond in SAME language as patient's transcript
- Only mention Paracetamol/PCM/Dolo 650 for fever and pain in low/moderate cases
- Always add "consult pharmacist or doctor before taking any medicine"
- Never suggest prescription medicines or antibiotics
- Never suggest dosages for children — say "consult doctor for children"
- Never diagnose specific diseases
- Keep response under 100 words
- Use simple language for rural users
- Be warm like a caring community health worker
"""

class Message(BaseModel):
    role: str
    content: str

class ResponseRequest(BaseModel):
    transcript: str
    symptoms: list[str]
    severity: str
    language: str = "te"
    history: list[Message] = []

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

@router.post("/generate-response")
async def generate_response(request: ResponseRequest):

    if not request.symptoms and not request.transcript:
        raise HTTPException(status_code=400, detail="No input provided")

    query = " ".join(request.symptoms) + " " + request.transcript
    context = retrieve_context(query, top_k=3)

    try:
        llm = get_llm()

        messages = [
            ("system", SYSTEM_PROMPT.format(
                context=context,
                symptoms=", ".join(request.symptoms) if request.symptoms else "general health query",
                severity=request.severity
            ))
        ]

        # Add conversation history
        for msg in request.history:
            if msg.role == "user":
                messages.append(("human", msg.content))
            else:
                messages.append(("ai", msg.content))

        # Add current message
        messages.append(("human", request.transcript))

        prompt = ChatPromptTemplate.from_messages(messages)
        chain = prompt | llm | StrOutputParser()

        response = await chain.ainvoke({})

        return {
            "response": response,
            "severity": request.severity
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Response generation error: {str(e)}")