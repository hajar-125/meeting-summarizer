from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil, os
from src.audio.transcriber import transcribe
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Meeting Summarizer")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # Sauvegarder le fichier uploadé
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Transcrire
    text = transcribe(path)
    return JSONResponse({"filename": file.filename, "transcription": text})