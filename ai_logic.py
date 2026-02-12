import os
from dotenv import load_dotenv
from google import genai
import json

# Încărcăm variabilele de mediu
load_dotenv()

def analyze_receipt(image_input):
    """
    Trimite imaginea la Gemini folosind noul SDK google-genai.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Eroare: Cheia API lipsește din .env")
        return None

    # Configurăm clientul
    client = genai.Client(api_key=api_key)

    prompt = """
    Ești un expert contabil. Analizează această imagine de bon fiscal.
    Extrage datele și returnează STRICT un JSON valid, fără ```json sau alte marcaje.
    Dacă imaginea nu este clară sau nu e un bon, returnează null.
    Formatul trebuie să fie:
    {
        "date": "YYYY-MM-DD",
        "amount": 0.00,
        "currency": "RON",
        "merchant": "Nume Magazin",
        "category": "Categorie (ex: Food, Transport, Utilities, Other)"
    }
    """

    try:
        # AICI AM SCHIMBAT: Folosim versiunea specifică 001, care e cea mai stabilă
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[prompt, image_input]
        )
        
        clean_text = response.text.strip()
        # Curățăm formatarea Markdown dacă există
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
            
        return json.loads(clean_text)
        
    except Exception as e:
        print(f"Eroare AI Detaliată: {e}")
        return None

if __name__ == "__main__":
    print("Logica AI actualizată la modelul gemini-1.5-flash-001.")