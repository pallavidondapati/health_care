from fastapi import APIRouter, UploadFile, File, HTTPException
from groq import Groq
from dotenv import load_dotenv
import os
import base64

load_dotenv()

router = APIRouter()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

VISION_PROMPT = """You are a medical image analyzer for rural India healthcare assistant VaaniCare.

Analyze this image and identify any visible health symptoms or conditions.

Look for:
- Skin conditions: rashes, wounds, burns, infections, discoloration, swelling
- Eye conditions: redness, discharge, swelling
- Visible injuries: cuts, bruises, fractures
- Oral conditions: if mouth is shown
- Any visible abnormalities

Return ONLY a JSON object:
{
  "symptoms_detected": ["list of visible symptoms in English"],
  "severity_hint": "mild | moderate | severe | null",
  "is_emergency": true or false,
  "description": "brief description of what you see in simple terms",
  "what_not_to_do": "one key warning if applicable or null",
  "advice": "immediate safe first aid advice in simple terms",
  "visit_doctor": true or false
}

Rules:
- NEVER diagnose diseases
- NEVER suggest medicine names
- If no health issue visible, return empty symptoms_detected
- If image is not medical, return empty symptoms_detected
- Be conservative — when in doubt say visit doctor
- Keep advice simple for rural users"""

@router.post("/analyze-photo")
async def analyze_photo(image: UploadFile = File(...)):

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file")

    if image.size and image.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large, max 10MB")

    try:
        image_data = await image.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        media_type = image.content_type or "image/jpeg"

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": VISION_PROMPT
                        }
                    ]
                }
            ],
            max_tokens=500,
            temperature=0
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        import json
        result = json.loads(raw)

        return {
            "symptoms_detected": result.get("symptoms_detected", []),
            "severity_hint": result.get("severity_hint"),
            "is_emergency": result.get("is_emergency", False),
            "description": result.get("description", ""),
            "what_not_to_do": result.get("what_not_to_do"),
            "advice": result.get("advice", ""),
            "visit_doctor": result.get("visit_doctor", True)
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Could not analyze image, please try again")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Photo analysis error: {str(e)}")