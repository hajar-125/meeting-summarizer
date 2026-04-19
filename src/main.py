from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil, os
from audio.transcriber import transcribe
from dotenv import load_dotenv

load_dotenv()

# Créer les dossiers nécessaires au démarrage
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

app = FastAPI(title="Meeting Summarizer")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    text = transcribe(path)
    return JSONResponse({"filename": file.filename, "transcription": text})