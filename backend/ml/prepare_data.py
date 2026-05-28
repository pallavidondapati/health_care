import json
import pandas as pd

# Training data — symptoms mapped to severity levels
# 0=low, 1=moderate, 2=high, 3=emergency
data = [
    # LOW
    {"text": "I have a mild headache", "label": 0},
    {"text": "I have a slight cold", "label": 0},
    {"text": "నాకు తేలికపాటి తలనొప్పి ఉంది", "label": 0},
    {"text": "నాకు జలుబు ఉంది", "label": 0},
    {"text": "मुझे हल्का सिरदर्द है", "label": 0},
    {"text": "I have a runny nose", "label": 0},
    {"text": "slight body ache", "label": 0},
    {"text": "నాకు కొంచెం దగ్గు ఉంది", "label": 0},
    {"text": "mild fever since morning", "label": 0},
    {"text": "मुझे थोड़ी खांसी है", "label": 0},

    # MODERATE
    {"text": "I have fever and cough for 2 days", "label": 1},
    {"text": "నాకు రెండు రోజులుగా జ్వరం మరియు దగ్గు ఉంది", "label": 1},
    {"text": "मुझे दो दिनों से बुखार है", "label": 1},
    {"text": "I have vomiting and diarrhea", "label": 1},
    {"text": "నాకు వాంతులు మరియు విరేచనాలు ఉన్నాయి", "label": 1},
    {"text": "body pain and high fever", "label": 1},
    {"text": "నాకు అధిక జ్వరం మరియు శరీర నొప్పి ఉంది", "label": 1},
    {"text": "मुझे उल्टी और दस्त हो रहे हैं", "label": 1},
    {"text": "I have stomach pain and nausea", "label": 1},
    {"text": "నాకు కడుపు నొప్పి ఉంది", "label": 1},

    # HIGH
    {"text": "I have severe chest pain", "label": 2},
    {"text": "నాకు తీవ్రమైన ఛాతీ నొప్పి ఉంది", "label": 2},
    {"text": "मुझे तेज सीने में दर्द है", "label": 2},
    {"text": "difficulty breathing since last night", "label": 2},
    {"text": "నాకు శ్వాస తీసుకోవడం కష్టంగా ఉంది", "label": 2},
    {"text": "high fever with seizures", "label": 2},
    {"text": "నాకు మూర్ఛలు వస్తున్నాయి", "label": 2},
    {"text": "मुझे सांस लेने में तकलीफ है", "label": 2},
    {"text": "severe abdominal pain", "label": 2},
    {"text": "నాకు తీవ్రమైన కడుపు నొప్పి ఉంది", "label": 2},

    # EMERGENCY
    {"text": "I cannot breathe at all", "label": 3},
    {"text": "నాకు అస్సలు శ్వాస రావడం లేదు", "label": 3},
    {"text": "मुझे बिल्कुल सांस नहीं आ रही", "label": 3},
    {"text": "patient is unconscious", "label": 3},
    {"text": "రోగి స్పృహ కోల్పోయాడు", "label": 3},
    {"text": "heart attack symptoms", "label": 3},
    {"text": "నాకు గుండె పోటు వచ్చినట్టు అనిపిస్తోంది", "label": 3},
    {"text": "severe bleeding that won't stop", "label": 3},
    {"text": "తీవ్రమైన రక్తస్రావం ఆగడం లేదు", "label": 3},
    {"text": "stroke symptoms face drooping", "label": 3},
]

df = pd.DataFrame(data)
df.to_csv("backend/ml/triage_data.csv", index=False)
print(f"Dataset created: {len(df)} samples")
print(df["label"].value_counts())