from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil, os
from audio.transcriber import transcribe
from processing.segmenter import segment_text
from processing.summarizer import summarize
from extraction.extractor import extract
from export.pdf_gen import generate_pdf
from export.mailer import send_summary_email
from export.notion_client import export_to_notion
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


@app.post("/summarize")
async def summarize_meeting(file: UploadFile = File(...)):
    """
    Pipeline complète : audio → transcription → résumé → plan d'action → exports
    """
    try:
        # 1. Sauvegarder le fichier
        path = f"uploads/{file.filename}"
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # 2. Transcrire
        transcription = transcribe(path)

        # 3. Segmenter
        segments = segment_text(transcription, mode="sentences")

        # 4. Résumer
        summary = summarize(segments)

        # 5. Extraire
        meeting = extract(segments, summary)

        # 6. Générer PDF
        pdf_path = generate_pdf(meeting)

        # 7. Exporter Notion
        notion_url = export_to_notion(meeting)

        # 8. Envoyer email
        send_summary_email(meeting, pdf_path)

        return JSONResponse({
            "status": "success",
            "transcription": transcription,
            "summary": meeting.summary,
            "decisions": meeting.decisions,
            "tasks": [t.dict() for t in meeting.tasks],
            "next_meeting": meeting.next_meeting,
            "notion_url": notion_url,
            "pdf_path": pdf_path
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))