"""Call Gemini API to summarize meeting segments."""
import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.1-flash-lite-preview"

def summarize(segments: list) -> str:
    full_text = "\n".join([f"[Segment {s['segment_id']}] {s['text']}" for s in segments])

    prompt = f"""
Tu es un assistant spécialisé dans l'analyse de réunions professionnelles.
Voici la transcription d'une réunion découpée en segments :

{full_text}

Génère un résumé exécutif structuré en français avec :
1. **Contexte** : de quoi parle cette réunion (2-3 phrases)
2. **Points clés discutés** : liste des sujets abordés
3. **Décisions prises** : liste des décisions actées
4. **Prochaines étapes** : ce qui a été planifié

Sois concis et professionnel.
"""

    print("[Summarizer] Envoi à Gemini...")
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    print("[Summarizer] Résumé reçu ✓")
    return response.text


def extract_action_plan(segments: list) -> dict:
    full_text = "\n".join([f"[Segment {s['segment_id']}] {s['text']}" for s in segments])

    prompt = f"""
Tu es un assistant spécialisé dans l'analyse de réunions professionnelles.
Voici la transcription d'une réunion :

{full_text}

Extrais UNIQUEMENT un objet JSON valide (sans markdown, sans backticks) avec cette structure exacte :
{{
  "decisions": ["décision 1", "décision 2"],
  "tasks": [
    {{"title": "nom de la tâche", "owner": "responsable", "deadline": "deadline ou null"}}
  ],
  "next_meeting": "date ou null"
}}

Réponds uniquement avec le JSON, rien d'autre.
"""

    print("[Summarizer] Extraction plan d'action via Gemini...")
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    action_plan = json.loads(text)
    print("[Summarizer] Plan d'action extrait ✓")
    return action_plan