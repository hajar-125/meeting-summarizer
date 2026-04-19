import os
import json
from google import genai
from dotenv import load_dotenv
from extraction.schemas import MeetingSummary, Task

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.1-flash-lite-preview"

def extract(segments: list, summary: str) -> MeetingSummary:
    full_text = "\n".join([f"[Segment {s['segment_id']}] {s['text']}" for s in segments])

    prompt = f"""
Tu es un assistant spécialisé dans l'analyse de réunions professionnelles.

Voici le résumé de la réunion :
{summary}

Voici la transcription complète :
{full_text}

Extrais UNIQUEMENT un objet JSON valide (sans markdown, sans backticks) avec cette structure :
{{
  "decisions": ["décision 1", "décision 2"],
  "tasks": [
    {{"title": "tâche", "owner": "responsable ou null", "deadline": "deadline ou null"}}
  ],
  "next_meeting": "date ou null"
}}

Règles importantes :
- Chaque décision doit être une phrase complète
- Chaque tâche doit avoir un titre clair et actionnable
- Ne jamais inventer des informations qui ne sont pas dans la transcription
- Réponds uniquement avec le JSON, rien d'autre
"""

    print("[Extractor] Extraction via Gemini...")
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"[Extractor] Erreur JSON : {e}")
        print(f"[Extractor] Réponse brute : {text}")
        raise

    # Valider avec Pydantic
    result = MeetingSummary(
        summary=summary,
        decisions=data.get("decisions", []),
        tasks=[Task(**t) for t in data.get("tasks", [])],
        next_meeting=data.get("next_meeting")
    )

    print(f"[Extractor] {len(result.decisions)} décision(s) · {len(result.tasks)} tâche(s) extraites ✓")
    return result