import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from processing.segmenter import segment_text
from processing.summarizer import summarize
from extraction.extractor import extract

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
summary = summarize(segments)
result = extract(segments, summary)

print("\n=== MEETING SUMMARY ===")
print(f"\nRésumé :\n{result.summary}")
print(f"\nDécisions :")
for d in result.decisions:
    print(f"  - {d}")
print(f"\nTâches :")
for t in result.tasks:
    print(f"  - {t.title} | Responsable: {t.owner} | Deadline: {t.deadline}")
print(f"\nProchain meeting : {result.next_meeting}")