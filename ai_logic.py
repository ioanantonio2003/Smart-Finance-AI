import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# Încărcăm cheia secretă din .env
load_dotenv()

# Configurăm Gemini cu cheia ta
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_receipt(image_data):
    """
    Trimite imaginea la Gemini și cere datele structurate (JSON).
    """
    # Alegem modelul 'gemini-1.5-flash' care e rapid și bun cu imaginile
    model = genai.GenerativeModel('gemini-1.5-flash')

    # PROMPT-ul: Instrucțiunile exacte pentru AI
    prompt = """
    Ești un expert contabil. Analizează această imagine de bon fiscal/factură.
    Extrage următoarele informații și returnează-le STRICT în format JSON, fără alte explicații:
    
    {
        "date": "data bonului în format YYYY-MM-DD (ex: 2024-02-12)",
        "amount": suma totală (număr float, ex: 125.50),
        "currency": "RON",
        "merchant": "numele magazinului",
        "category": "alege una din: [Mâncare, Transport, Utilități, Haine, Altele]"
    }

    Dacă nu poți citi bonul sau nu e un bon, returnează un JSON cu valori null.
    Nu pune ```json la început sau sfârșit, dă-mi doar textul brut JSON.
    """

    try:
        # Trimitem promptul + imaginea la AI
        response = model.generate_content([prompt, image_data])
        
        # Curățăm răspunsul (uneori AI-ul mai pune spații sau caractere extra)
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        
        # Transformăm textul în dicționar Python
        return json.loads(clean_text)
        
    except Exception as e:
        print(f"Eroare AI: {e}")
        return None

# Test rapid (doar dacă rulăm acest fișier direct)
if __name__ == "__main__":
    print("Acest fișier conține logica AI. Rulează 'app.py' pentru interfață.")