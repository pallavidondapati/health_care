from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter()

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    severity: str = "moderate"

FACILITY_TYPE_MAP = {
    "low": "pharmacy",
    "moderate": "primary health centre",
    "high": "hospital",
    "emergency": "emergency hospital"
}

@router.post("/nearest-facility")
async def nearest_facility(request: LocationRequest):

    if not (-90 <= request.latitude <= 90) or not (-180 <= request.longitude <= 180):
        raise HTTPException(status_code=400, detail="Invalid coordinates")

    facility_type = FACILITY_TYPE_MAP.get(request.severity, "hospital")

    # OpenStreetMap Overpass API — completely free, no key needed
    overpass_query = f"""
    [out:json][timeout:10];
    (
      node["amenity"="hospital"](around:10000,{request.latitude},{request.longitude});
      node["amenity"="clinic"](around:10000,{request.latitude},{request.longitude});
      node["amenity"="health_post"](around:10000,{request.latitude},{request.longitude});
      node["healthcare"="centre"](around:10000,{request.latitude},{request.longitude});
    );
    out body 5;
    """

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://overpass-api.de/api/interpreter",
                data=overpass_query
            )
            data = response.json()

        facilities = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name") or tags.get("name:en") or tags.get("name:te") or "Health Facility"
            lat = element.get("lat")
            lon = element.get("lon")

            if lat and lon:
                # Calculate rough distance in km
                distance = round((
                    ((lat - request.latitude) ** 2 +
                     (lon - request.longitude) ** 2) ** 0.5
                ) * 111, 2)

                facilities.append({
                    "name": name,
                    "type": tags.get("amenity") or tags.get("healthcare", "health facility"),
                    "latitude": lat,
                    "longitude": lon,
                    "distance_km": distance,
                    "phone": tags.get("phone") or tags.get("contact:phone") or None,
                    "google_maps": f"https://www.google.com/maps?q={lat},{lon}"
                })

        # Sort by distance
        facilities.sort(key=lambda x: x["distance_km"])

        # Emergency always show nearest hospital + 108
        if request.severity == "emergency":
            return {
                "severity": "emergency",
                "call_108": True,
                "message": "🚨 Call 108 immediately! Nearest facilities:",
                "facilities": facilities[:3]
            }

        return {
            "severity": request.severity,
            "call_108": False,
            "recommended_facility_type": facility_type,
            "facilities": facilities[:5]
        }

    except httpx.TimeoutException:
        return {
        "severity": request.severity,
        "call_108": request.severity == "emergency",
        "recommended_facility_type": facility_type,
        "facilities": []
    }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Facility search error: {str(e)}")