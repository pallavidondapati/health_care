MEDICAL_KNOWLEDGE = [
    # FEVER
    {
        "id": "fever_001",
        "topic": "fever causes treatment medicine",
        "content": """Fever (జ్వరం/बुखार) — Temperature above 38°C.
CAUSES: Viral infections (cold, flu), bacterial infections, malaria, dengue, typhoid, heat exhaustion.
HOME REMEDIES: Drink plenty of water and fluids. Apply cool wet cloth on forehead. Drink warm tulsi-ginger tea. Eat light food like rice porridge (ganji/khichdi).
MEDICINE (Low fever only): Paracetamol/PCM/Dolo 650 — 1 tablet for adults when fever above 38°C. Max 4 tablets per day. Consult pharmacist before taking.
WHAT NOT TO DO: Do not cover with heavy blankets. Do not give Aspirin to children. Do not stop eating completely. Do not ignore fever lasting more than 3 days.
VISIT DOCTOR IF: Fever above 39.5°C, lasts more than 3 days, comes with rash, severe headache, or difficulty breathing."""
    },
    # COUGH
    {
        "id": "cough_001",
        "topic": "cough causes treatment",
        "content": """Cough (దగ్గు/खांसी) — Can be dry or wet.
CAUSES: Viral infection, dust allergy, asthma, bacterial infection, acid reflux, tuberculosis (if chronic).
HOME REMEDIES: Drink warm water with honey and ginger 3 times daily. Gargle with warm salt water. Steam inhalation twice daily. Drink turmeric milk at night.
MEDICINE: For dry cough, pharmacist may suggest OTC cough syrup. Consult pharmacist before taking.
WHAT NOT TO DO: Do not drink cold water or cold drinks. Do not expose to dust and smoke. Do not ignore cough with blood.
VISIT DOCTOR IF: Cough lasts more than 3 weeks, produces blood, comes with chest pain or breathing difficulty."""
    },
    # COLD
    {
        "id": "cold_001",
        "topic": "cold runny nose causes treatment",
        "content": """Cold (జలుబు/सर्दी) — Very common viral infection.
CAUSES: Rhinovirus, seasonal changes, weak immunity, exposure to cold or rain.
HOME REMEDIES: Drink warm turmeric milk at night. Inhale steam with eucalyptus oil. Drink ginger tulsi tea 3 times daily. Rest well and sleep 8 hours.
MEDICINE: Paracetamol/Dolo 650 for body ache and mild fever. Consult pharmacist for safe decongestant.
WHAT NOT TO DO: Do not drink cold water. Do not go out in cold wind. Do not take antibiotics — cold is viral, antibiotics don't work.
VISIT DOCTOR IF: Cold lasts more than 10 days, causes ear pain, high fever, or difficulty breathing."""
    },
    # SORE THROAT
    {
        "id": "throat_001",
        "topic": "sore throat causes treatment",
        "content": """Sore Throat (గొంతు నొప్పి/गले में दर्द).
CAUSES: Viral infection, bacterial infection (strep throat), pollution, excessive talking, acid reflux.
HOME REMEDIES: Gargle warm salt water 4 times daily. Drink warm water with honey and ginger. Drink warm turmeric milk at night. Avoid cold drinks completely.
MEDICINE: Paracetamol for pain relief. Consult pharmacist for throat lozenges. Do not self-medicate with antibiotics.
WHAT NOT TO DO: Do not drink cold water or cold drinks. Do not eat spicy food. Do not strain voice. Do not take antibiotics without doctor prescription.
VISIT DOCTOR IF: White patches on throat, very severe pain, high fever above 39°C, difficulty swallowing."""
    },
    # STOMACH PAIN
    {
        "id": "stomach_001",
        "topic": "stomach pain causes treatment",
        "content": """Stomach Pain (కడుపు నొప్పి/पेट दर्द).
CAUSES: Indigestion, gas, acidity, food poisoning, gastritis, appendicitis (right lower side), menstrual cramps, kidney stones.
HOME REMEDIES: Drink warm water with hing (asafoetida) pinch. Drink ginger tea. Apply warm cloth on stomach. Eat light food — khichdi, plain rice, banana. Avoid spicy oily food.
MEDICINE: Antacid for acidity-related pain — consult pharmacist. Do not take painkillers on empty stomach.
WHAT NOT TO DO: Do not eat spicy oily food. Do not drink alcohol. Do not ignore severe pain in lower right side — could be appendicitis emergency.
VISIT DOCTOR IF: Pain is severe, located lower right side, comes with fever, lasts more than 2 days, or has vomiting and diarrhea together."""
    },
    # DIARRHEA / LOOSE MOTIONS
    {
        "id": "diarrhea_001",
        "topic": "diarrhea loose motions causes treatment ORS",
        "content": """Diarrhea/Loose Motions (విరేచనాలు/दस्त).
CAUSES: Food poisoning, contaminated water, viral or bacterial infection, stress, lactose intolerance.
HOME REMEDIES: ORS immediately — mix 1 liter clean boiled water + 6 teaspoons sugar + half teaspoon salt. Drink throughout day. Eat banana, plain rice, curd, boiled potato. Drink coconut water.
MEDICINE: ORS packets available at any pharmacy or PHC — free at government PHC. Consult pharmacist for safe antidiarrheal medicine for adults.
WHAT NOT TO DO: Do not eat spicy or oily food. Do not drink unboiled water. Do not take antibiotics without doctor advice. Do not ignore severe dehydration signs.
VISIT DOCTOR IF: Diarrhea has blood, lasts more than 2 days, child or elderly person affected, signs of severe dehydration — sunken eyes, not urinating."""
    },
    # VOMITING
    {
        "id": "vomiting_001",
        "topic": "vomiting nausea causes treatment",
        "content": """Vomiting/Nausea (వాంతులు/उल्टी).
CAUSES: Food poisoning, viral infection, motion sickness, pregnancy, migraine, gastritis, eating too fast.
HOME REMEDIES: Stop solid food for 2 hours. Sip small amounts of ORS every 15 minutes. Chew small piece of ginger or sip ginger tea. When vomiting stops, eat banana or plain rice slowly.
MEDICINE: Consult pharmacist for safe anti-nausea medicine. Do not take medicine on empty stomach.
WHAT NOT TO DO: Do not eat solid food immediately after vomiting. Do not lie flat — sit upright. Do not drink large amounts of water at once. Do not ignore vomiting blood.
VISIT DOCTOR IF: Vomiting continues more than 24 hours, has blood, patient cannot drink water at all, comes with severe stomach pain or high fever."""
    },
    # HEADACHE
    {
        "id": "headache_001",
        "topic": "headache causes treatment medicine",
        "content": """Headache (తలనొప్పి/सिरदर्द).
CAUSES: Dehydration, stress, lack of sleep, eye strain, sinusitis, high blood pressure, migraine, tension.
HOME REMEDIES: Drink 2-3 glasses of water immediately. Rest in quiet dark room. Apply cold or warm cloth on forehead. Gently massage temples with coconut or sesame oil. Sleep well.
MEDICINE: Paracetamol/Dolo 650 — 1 tablet for adults. Consult pharmacist before taking. Do not take painkillers frequently.
WHAT NOT TO DO: Do not stare at phone or screen. Do not skip meals. Do not ignore headache with fever and stiff neck — could be meningitis emergency. Do not take painkillers more than 3 days continuously.
VISIT DOCTOR IF: Sudden severe headache (worst of life), headache with fever and stiff neck, after head injury, with vision changes or weakness."""
    },
    # BODY PAIN
    {
        "id": "body_pain_001",
        "topic": "body pain weakness fatigue causes treatment",
        "content": """Body Pain/Weakness (శరీర నొప్పి/बदन दर्द).
CAUSES: Viral fever, overwork, poor nutrition, dehydration, malaria, dengue, chikungunya, anemia.
HOME REMEDIES: Rest completely for 1-2 days. Drink plenty of fluids. Warm water bath helps relieve pain. Eat nutritious food with protein — dal, eggs, green vegetables. Sleep 8 hours.
MEDICINE: Paracetamol/Dolo 650 for pain relief — consult pharmacist. If weakness is due to anemia, iron-rich foods like spinach, dates, jaggery help.
WHAT NOT TO DO: Do not do heavy physical work. Do not ignore weakness lasting more than a week. Do not skip meals.
VISIT DOCTOR IF: Body pain with high fever and chills (could be malaria), severe weakness, joint pain with rash, lasts more than 5 days."""
    },
    # ACIDITY
    {
        "id": "acidity_001",
        "topic": "acidity heartburn causes treatment",
        "content": """Acidity/Heartburn (యాసిడిటీ/एसिडिटी).
CAUSES: Spicy oily food, skipping meals, stress, excess tea/coffee, smoking, alcohol, lying down after eating.
HOME REMEDIES: Drink cold milk or buttermilk. Eat small frequent meals. Drink coconut water. Eat banana. Avoid spicy oily food. Don't lie down for 2 hours after eating.
MEDICINE: Antacid available at pharmacy — consult pharmacist. Common OTC antacids give quick relief. Do not take on empty stomach.
WHAT NOT TO DO: Do not eat spicy oily food. Do not drink excess tea or coffee. Do not smoke. Do not take painkillers like ibuprofen on empty stomach. Do not lie flat immediately after eating.
VISIT DOCTOR IF: Acidity is frequent and severe, comes with difficulty swallowing, chest pain, or blood in vomit."""
    },
    # DEHYDRATION
    {
        "id": "dehydration_001",
        "topic": "dehydration ORS treatment",
        "content": """Dehydration (నీరసం/निर्जलीकरण).
CAUSES: Diarrhea, vomiting, fever, excessive sweating, not drinking enough water, hot weather.
HOME REMEDIES: ORS — mix 1 liter boiled cooled water + 6 teaspoons sugar + half teaspoon salt. Drink coconut water, buttermilk, rice water. Rest in cool place.
MEDICINE: ORS packets free at government PHC. Available at any pharmacy.
WHAT NOT TO DO: Do not drink sugary sodas or cold drinks. Do not wait if child is severely dehydrated. Do not ignore signs of severe dehydration.
VISIT DOCTOR IF: Sunken eyes, dry mouth, not urinating for 6+ hours, very weak, confused — needs IV fluids at hospital immediately."""
    },
    # MALARIA
    {
        "id": "malaria_001",
        "topic": "malaria fever chills causes treatment",
        "content": """Malaria (మలేరియా/मलेरिया).
CAUSES: Plasmodium parasite spread by Anopheles mosquito bite. Common during and after monsoon season.
SYMPTOMS: Cyclical fever with chills and sweating, severe headache, body pain, vomiting.
HOME REMEDIES: Drink plenty of fluids. Cover yourself during chills. Rest completely.
MEDICINE: Do NOT self-medicate for malaria. Needs blood test and specific antimalarial medicines prescribed by doctor.
WHAT NOT TO DO: Do not ignore cyclical fever in monsoon season. Do not self-medicate. Do not sleep without mosquito net.
PREVENTION: Use mosquito nets, mosquito repellent, remove stagnant water near home.
VISIT DOCTOR: Immediately for blood test and treatment. Free treatment available at government PHC."""
    },
    # DENGUE
    {
        "id": "dengue_001",
        "topic": "dengue fever treatment",
        "content": """Dengue Fever (డెంగీ/डेंगू).
CAUSES: Dengue virus spread by Aedes mosquito — bites during daytime.
SYMPTOMS: Sudden high fever, severe headache, pain behind eyes, joint and muscle pain, rash, mild bleeding from gums or nose.
HOME REMEDIES: Rest completely. Drink plenty of fluids — coconut water, ORS, fresh juices. Papaya leaf juice may help platelet count.
MEDICINE: Paracetamol for fever only. Do NOT take Aspirin or Ibuprofen — increases bleeding risk.
WHAT NOT TO DO: Do not take Aspirin or Ibuprofen. Do not ignore bleeding signs. Do not skip fluid intake.
VISIT DOCTOR: Immediately for platelet count blood test. If bleeding occurs — go to hospital emergency."""
    },
    # CHEST PAIN EMERGENCY
    {
        "id": "chest_001",
        "topic": "chest pain heart attack emergency",
        "content": """Chest Pain (ఛాతీ నొప్పి/सीने में दर्द) — EMERGENCY.
CAUSES: Heart attack, angina, pulmonary embolism, pneumonia, severe acidity, muscle strain.
ANY CHEST PAIN IS AN EMERGENCY — Call 108 immediately.
Do not drive yourself. Sit upright and rest. Loosen tight clothing. Do not eat or drink.
WHAT NOT TO DO: Do not ignore chest pain. Do not walk around. Do not try home remedies.
Call 108 now."""
    },
    # BREATHING DIFFICULTY
    {
        "id": "breathing_001",
        "topic": "breathing difficulty emergency asthma",
        "content": """Breathing Difficulty (శ్వాస తీసుకోవడం కష్టం/सांस लेने में तकलीफ) — EMERGENCY.
CAUSES: Asthma attack, severe allergic reaction, pneumonia, heart failure, COVID, choking.
EMERGENCY: Call 108 immediately. Sit upright. Open windows. Loosen tight clothing. If asthma — use inhaler immediately.
WHAT NOT TO DO: Do not lie flat. Do not panic. Do not try home remedies for severe breathing difficulty.
Go to nearest hospital emergency immediately."""
    },
    # DIABETES
    {
        "id": "diabetes_001",
        "topic": "diabetes symptoms management",
        "content": """Diabetes (మధుమేహం/मधुमेह).
CAUSES: Insulin resistance or deficiency. Risk factors — obesity, family history, unhealthy diet, sedentary lifestyle.
SYMPTOMS: Excessive thirst, frequent urination, unexplained weight loss, blurred vision, slow healing wounds, fatigue.
HOME REMEDIES: Eat low sugar diet — less rice, more vegetables, whole grains. Walk 30 minutes daily. Bitter gourd (karela) juice may help.
MEDICINE: Diabetes needs proper diagnosis and doctor-prescribed medicines. Do NOT self-medicate.
WHAT NOT TO DO: Do not eat sweets, white rice, maida in excess. Do not skip meals. Do not stop prescribed medicines without doctor advice.
VISIT DOCTOR: Visit PHC for blood sugar test. Free diabetes medicines at government hospitals under National Health Mission."""
    },
    # SNAKE BITE
    {
        "id": "snakebite_001",
        "topic": "snake bite emergency treatment",
        "content": """Snake Bite (పాము కాటు/सांप का काटना) — EMERGENCY.
Keep patient calm and completely still — movement spreads venom faster.
Remove jewelry and tight clothing near bite area.
DO NOT: Cut the wound. Suck the venom. Apply tourniquet. Apply ice or heat.
Immobilize bitten limb below heart level.
Call 108 immediately. Go to nearest hospital for antivenom. Time is critical — every minute counts."""
    },
    # MENTAL HEALTH
    {
        "id": "mental_001",
        "topic": "mental health depression anxiety stress",
        "content": """Mental Health (మానసిక ఆరోగ్యం/मानसिक स्वास्थ्य).
CAUSES: Stress, trauma, family problems, financial stress, chronic illness, loneliness.
SYMPTOMS: Persistent sadness, loss of interest, sleep problems, hopelessness, anxiety, irritability.
HOME REMEDIES: Talk to trusted family member or friend. Walk in fresh air daily. Practice slow deep breathing. Maintain regular sleep schedule. Eat regular healthy meals.
WHAT NOT TO DO: Do not isolate yourself. Do not use alcohol to cope. Do not ignore symptoms for weeks.
HELP: iCall helpline — 9152987821. Vandrevala Foundation — 1860-2662-345 (24/7 free). Visit PHC for referral to mental health services. Free treatment under Ayushman Bharat."""
    },
    # PREGNANCY
    {
        "id": "pregnancy_001",
        "topic": "pregnancy danger signs",
        "content": """Pregnancy Danger Signs (గర్భధారణ ప్రమాద సంకేతాలు).
EMERGENCY SIGNS — Go to PHC or hospital immediately:
Heavy bleeding, severe stomach pain, severe headache with vision changes, swollen face and hands, convulsions/fits, reduced baby movement for more than a day, high fever, water breaking before 37 weeks.
WHAT NOT TO DO: Do not take any medicine without doctor advice during pregnancy. Do not ignore danger signs. Do not deliver at home without trained health worker.
Call 108 or go to nearest PHC/CHC/government hospital immediately. Free delivery under Janani Suraksha Yojana."""
    },
    # PREVENTION
    {
        "id": "prevention_001",
        "topic": "preventive healthcare government schemes",
        "content": """Preventive Healthcare and Government Schemes.
PREVENTION TIPS: Wash hands with soap before eating and after toilet. Drink only boiled or filtered water. Eat fresh vegetables and fruits daily. Use mosquito nets. Get children vaccinated on time. Exercise 30 minutes daily.
GOVERNMENT SCHEMES: Ayushman Bharat PMJAY — free treatment up to 5 lakhs at empanelled hospitals. Free medicines at Jan Aushadhi Kendras. Free diagnostics at government hospitals. ASHA workers available in every village for health guidance. Call 104 for health helpline. Call 108 for emergency ambulance."""
    },
]