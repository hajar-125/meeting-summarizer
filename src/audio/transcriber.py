import os

WHISPER_BACKEND = os.getenv("WHISPER_BACKEND", "mlx")

def transcribe(audio_path: str) -> str:
    print(f"[Transcriber] Backend: {WHISPER_BACKEND} | Fichier: {audio_path}")
    
    if WHISPER_BACKEND == "mlx":
        import mlx_whisper
        result = mlx_whisper.transcribe(
            audio_path,
            path_or_hf_repo="mlx-community/whisper-base"
        )
        return result["text"]
    else:
        import whisper
        model = whisper.load_model("base")
        return model.transcribe(audio_path)["text"]