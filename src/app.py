import streamlit as st
import os, sys, shutil, json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from audio.transcriber import transcribe
from processing.segmenter import segment_text
from processing.summarizer import summarize, extract_action_plan
from extraction.extractor import extract
from export.pdf_gen import generate_pdf
from export.mailer import send_summary_email
from export.notion_client import export_to_notion

# ── Config page ──
st.set_page_config(
    page_title="Meeting Summarizer",
    page_icon="📋",
    layout="wide"
)

# ── CSS custom ──
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f, #2d6a9f);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .step-box {
        background: #f4f7fb;
        border-left: 4px solid #1e3a5f;
        padding: 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    .success-box {
        background: #eaf3e0;
        border-left: 4px solid #2d6a2d;
        padding: 1rem;
        border-radius: 4px;
    }
    .decision-item {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="main-header">
    <h1>📋 Meeting Summarizer</h1>
    <p>Transcription automatique · Résumé IA · Plan d'action · Export PDF / Email / Notion</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ──
if "transcription" not in st.session_state:
    st.session_state.transcription = None
if "segments" not in st.session_state:
    st.session_state.segments = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "meeting" not in st.session_state:
    st.session_state.meeting = None
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

# ════════════════════════════════════════
# ÉTAPE 1 — Upload & Transcription
# ════════════════════════════════════════
st.header("🎙️ Étape 1 — Upload & Transcription")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Importe ton fichier audio ou vidéo",
        type=["mp3", "mp4", "wav", "m4a", "aiff"],
        help="Formats supportés : mp3, mp4, wav, m4a, aiff"
    )

with col2:
    st.markdown("**Ou colle une transcription directement :**")
    manual_text = st.text_area(
        "Transcription manuelle",
        height=120,
        placeholder="Colle ici le texte de ta réunion...",
        label_visibility="collapsed"
    )

if uploaded_file:
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{uploaded_file.name}"
    with open(path, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)

    if st.button("🎯 Lancer la transcription", type="primary"):
        with st.spinner("Transcription en cours avec Whisper..."):
            try:
                st.session_state.transcription = transcribe(path)
                st.success("✅ Transcription terminée !")
            except Exception as e:
                st.error(f"Erreur : {e}")

elif manual_text:
    if st.button("✅ Utiliser ce texte", type="primary"):
        st.session_state.transcription = manual_text
        st.success("✅ Texte chargé !")

if st.session_state.transcription:
    with st.expander("📄 Voir la transcription complète"):
        st.text_area(
            "Transcription",
            value=st.session_state.transcription,
            height=200,
            label_visibility="collapsed"
        )

# ════════════════════════════════════════
# ÉTAPE 2 — Résumé & Extraction
# ════════════════════════════════════════
if st.session_state.transcription:
    st.divider()
    st.header("🧠 Étape 2 — Résumé & Extraction IA")

    col1, col2 = st.columns(2)
    with col1:
        mode = st.selectbox(
            "Mode de segmentation",
            ["sentences", "keywords"],
            help="sentences = découpage par phrases | keywords = découpage par mots-clés"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Analyser avec Gemini", type="primary"):
            with st.spinner("Segmentation..."):
                st.session_state.segments = segment_text(
                    st.session_state.transcription, mode=mode
                )
            with st.spinner("Génération du résumé..."):
                st.session_state.summary = summarize(st.session_state.segments)
            with st.spinner("Extraction du plan d'action..."):
                st.session_state.meeting = extract(
                    st.session_state.segments,
                    st.session_state.summary
                )
            st.success("✅ Analyse terminée !")

    if st.session_state.meeting:
        meeting = st.session_state.meeting

        # Résumé
        st.subheader("📝 Résumé exécutif")
        clean = meeting.summary.replace("**", "").replace("*", "").replace("#", "")
        st.markdown(f"""<div class="step-box">{clean}</div>""", unsafe_allow_html=True)

        # Décisions
        st.subheader("✅ Décisions prises")
        for d in meeting.decisions:
            st.markdown(f"""<div class="decision-item">• {d}</div>""", unsafe_allow_html=True)

        # Tâches
        st.subheader("🎯 Plan d'action")
        if meeting.tasks:
            import pandas as pd
            tasks_data = [{
                "Tâche": t.title,
                "Responsable": t.owner or "—",
                "Deadline": t.deadline or "—"
            } for t in meeting.tasks]
            st.dataframe(
                pd.DataFrame(tasks_data),
                use_container_width=True,
                hide_index=True
            )

        # Prochain meeting
        if meeting.next_meeting:
            st.info(f"📅 Prochain meeting : **{meeting.next_meeting}**")

# ════════════════════════════════════════
# ÉTAPE 3 — Exports
# ════════════════════════════════════════
if st.session_state.meeting:
    st.divider()
    st.header("📤 Étape 3 — Exports")

    col_pdf, col_email, col_notion = st.columns(3)

    # ── PDF ──
    with col_pdf:
        st.subheader("📄 PDF")
        if st.button("Générer le PDF", type="primary", use_container_width=True):
            with st.spinner("Génération du PDF..."):
                try:
                    os.makedirs("outputs", exist_ok=True)
                    st.session_state.pdf_path = generate_pdf(st.session_state.meeting)
                    st.success("✅ PDF généré !")
                except Exception as e:
                    st.error(f"Erreur : {e}")

        if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
            with open(st.session_state.pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Télécharger le PDF",
                    data=f,
                    file_name=f"compte_rendu_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

    # ── Email ──
    with col_email:
        st.subheader("📧 Email")
        receiver = st.text_input(
            "Destinataire",
            placeholder="email@exemple.com",
            label_visibility="visible"
        )
        if st.button("Envoyer l'email", type="primary", use_container_width=True):
            if not receiver:
                st.warning("Entre un email destinataire")
            elif not st.session_state.pdf_path:
                st.warning("Génère d'abord le PDF")
            else:
                with st.spinner("Envoi en cours..."):
                    try:
                        os.environ["EMAIL_RECEIVER"] = receiver
                        send_summary_email(
                            st.session_state.meeting,
                            st.session_state.pdf_path
                        )
                        st.success(f"✅ Email envoyé à {receiver} !")
                    except Exception as e:
                        st.error(f"Erreur : {e}")

    # ── Notion ──
    with col_notion:
        st.subheader("📓 Notion")
        if st.button("Exporter vers Notion", type="primary", use_container_width=True):
            with st.spinner("Export Notion..."):
                try:
                    url = export_to_notion(st.session_state.meeting)
                    st.success("✅ Page créée !")
                    st.markdown(f"[🔗 Ouvrir dans Notion]({url})")
                except Exception as e:
                    st.error(f"Erreur : {e}")

# ── Footer ──
st.divider()
st.markdown(
    "<p style='text-align:center;color:#aaa;font-size:12px'>"
    "Meeting Summarizer — généré automatiquement par IA · Whisper + Gemini"
    "</p>",
    unsafe_allow_html=True
)