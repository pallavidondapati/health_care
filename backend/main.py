from fastapi import FastAPI
from backend.api.speech import router as speech_router
from backend.api.symptom import router as symptom_router
from backend.api.triage import router as triage_router
from backend.api.safety import router as safety_router
from backend.api.response import router as response_router
from backend.api.tts import router as tts_router
from backend.api.facility import router as facility_router
from backend.api.vaanicare import router as vaanicare_router

app = FastAPI(
    title="VaaniCare API",
    description="Multilingual voice ai health assistant",
    version="1.0"
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
from backend.api.photo import router as photo_router
app.include_router(photo_router, prefix="/api")
app.include_router(speech_router, prefix="/api")
app.include_router(symptom_router, prefix="/api")
app.include_router(triage_router, prefix="/api")
app.include_router(safety_router, prefix="/api")
app.include_router(response_router, prefix="/api")
app.include_router(tts_router, prefix="/api")
app.include_router(facility_router, prefix="/api")
app.include_router(vaanicare_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "VaaniCare Backend Running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}