import os

WHISPER_BACKEND = os.getenv("WHISPER_BACKEND", "faster")

def transcribe(audio_path: str) -> str:
    print(f"[Transcriber] Backend: {WHISPER_BACKEND}")
    print(f"[Transcriber] Fichier : {audio_path}")

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")

    if WHISPER_BACKEND == "mlx":
        import mlx_whisper
        result = mlx_whisper.transcribe(
            audio_path,
            path_or_hf_repo="mlx-community/whisper-base"
        )
        return result["text"].strip()

    else:
        from faster_whisper import WhisperModel
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_path)
        return " ".join([seg.text for seg in segments]).strip()