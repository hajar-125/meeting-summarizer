import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from processing.segmenter import segment_text
from processing.summarizer import summarize
from extraction.extractor import extract
from export.notion_client import export_to_notion

texte = """
Bonjour à tous. Aujourd'hui on discute du projet résumeur de réunion.
On a décidé d'utiliser Whisper pour la transcription et FastAPI comme backend.
Hajar s'occupe de la transcription et de l'intégration Gemini.
Le binôme gère les exports PDF et Notion. Deadline fixée à vendredi.
Le prochain point de synchronisation est jeudi matin.
"""

segments = segment_text(texte, mode="sentences")
summary  = summarize(segments)
result   = extract(segments, summary)

print("\n=== EXPORT NOTION ===")
url = export_to_notion(result)
print(f"Page disponible : {url}")