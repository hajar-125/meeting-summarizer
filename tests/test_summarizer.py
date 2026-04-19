import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from processing.segmenter import segment_text
from processing.summarizer import summarize, extract_action_plan

texte = """
Bonjour à tous. Aujourd'hui on discute du projet résumeur de réunion.
Premier point : le choix de la technologie. On a décidé d'utiliser Whisper pour la transcription.
Ensuite on a parlé de l'architecture. La décision prise est d'utiliser FastAPI comme backend.
Passons au point suivant. Les tâches assignées sont les suivantes.
Hajar s'occupe de la transcription et de l'intégration Gemini.
Le binôme gère les exports PDF et Notion. Deadline fixée à vendredi.
Pour conclure, le prochain point de synchronisation est jeudi matin.
"""

segments = segment_text(texte, mode="sentences")

print("=== RÉSUMÉ ===")
resume = summarize(segments)
print(resume)

print("\n=== PLAN D'ACTION ===")
plan = extract_action_plan(segments)
import json
print(json.dumps(plan, ensure_ascii=False, indent=2))