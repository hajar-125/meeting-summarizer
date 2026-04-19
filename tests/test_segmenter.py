import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from processing.segmenter import segment_text

# Texte simulant une transcription réelle
texte = """
Bonjour à tous. Aujourd'hui on discute du projet résumeur de réunion.
Premier point : le choix de la technologie. On a décidé d'utiliser Whisper pour la transcription.
Ensuite on a parlé de l'architecture. La décision prise est d'utiliser FastAPI comme backend.
Passons au point suivant. Les tâches assignées sont les suivantes.
Hajar s'occupe de la transcription et de l'intégration Claude.
Le binôme gère les exports PDF et Notion. Deadline fixée à vendredi.
Pour conclure, le prochain point de synchronisation est jeudi matin.
"""

print("=== MODE SENTENCES ===")
segments = segment_text(texte, mode="sentences")
for s in segments:
    print(f"\n[Segment {s['segment_id']}]")
    print(s['text'])

print("\n=== MODE KEYWORDS ===")
segments = segment_text(texte, mode="keywords")
for s in segments:
    print(f"\n[Segment {s['segment_id']}]")
    print(s['text'])