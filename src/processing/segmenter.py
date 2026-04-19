"""Segment transcribed text into logical chunks."""
import re
from typing import List, Dict

def segment_by_sentences(text: str, chunk_size: int = 5) -> List[Dict]:
    """
    Découpe le texte en segments de N phrases.
    Retourne une liste de blocs numérotés.
    """
    # Découper par ponctuation de fin de phrase
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    segments = []
    for i in range(0, len(sentences), chunk_size):
        chunk = sentences[i:i + chunk_size]
        segments.append({
            "segment_id": i // chunk_size + 1,
            "text": " ".join(chunk),
            "sentence_count": len(chunk)
        })

    return segments


def segment_by_keywords(text: str) -> List[Dict]:
    keywords = [
        "ensuite", "maintenant", "passons à", "point suivant",
        "autre sujet", "pour conclure", "en résumé", "décision",
        "action", "responsable", "deadline", "prochain"
    ]

    # Découper sur le mot-clé en le gardant dans le segment suivant
    pattern = r'(?i)(?<=[.!?,])\s+(?=' + '|'.join(keywords) + r'\b)'
    parts = re.split(pattern, text.strip())
    parts = [p.strip() for p in parts if p.strip()]

    segments = []
    for i, part in enumerate(parts):
        segments.append({
            "segment_id": i + 1,
            "text": part,
            "sentence_count": len(re.split(r'[.!?]', part))
        })

    return segments

def segment_text(text: str, mode: str = "sentences") -> List[Dict]:
    """
    Point d'entrée principal.
    mode: 'sentences' ou 'keywords'
    """
    print(f"[Segmenter] Mode: {mode} | Texte: {len(text)} caractères")

    if mode == "keywords":
        segments = segment_by_keywords(text)
    else:
        segments = segment_by_sentences(text)

    print(f"[Segmenter] {len(segments)} segment(s) générés")
    return segments