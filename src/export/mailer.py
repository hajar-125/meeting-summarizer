"""Email sending using smtplib or SendGrid."""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from dotenv import load_dotenv
from extraction.schemas import MeetingSummary

load_dotenv()

def send_summary_email(meeting: MeetingSummary, pdf_path: str) -> bool:
    """
    Envoie le résumé de réunion par email avec le PDF en pièce jointe.
    """
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    receiver  = os.getenv("EMAIL_RECEIVER")

    if not all([smtp_user, smtp_pass, receiver]):
        raise ValueError("Variables SMTP manquantes dans .env")

    # ── Construire l'email ──
    msg = MIMEMultipart()
    msg["From"]    = smtp_user
    msg["To"]      = receiver
    msg["Subject"] = f"Compte-rendu de réunion — {datetime.now().strftime('%d/%m/%Y')}"

    # ── Corps HTML ──
    decisions_html = "".join([f"<li>{d}</li>" for d in meeting.decisions])
    tasks_html = "".join([f"""
        <tr>
            <td style='padding:6px 10px;border-bottom:1px solid #eee'>{t.title}</td>
            <td style='padding:6px 10px;border-bottom:1px solid #eee'>{t.owner or '—'}</td>
            <td style='padding:6px 10px;border-bottom:1px solid #eee'>{t.deadline or '—'}</td>
        </tr>
    """ for t in meeting.tasks])

    body = f"""
    <html><body style='font-family:Arial,sans-serif;color:#1a1a1a;max-width:600px;margin:auto'>
        <div style='background:#1e3a5f;color:white;padding:20px;border-radius:8px 8px 0 0'>
            <h2 style='margin:0'>📋 Compte-rendu de réunion</h2>
            <p style='margin:4px 0 0;opacity:0.75;font-size:13px'>
                Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
            </p>
        </div>

        <div style='padding:20px;background:#f9fafc;border:1px solid #e0e0e0'>
            <h3 style='color:#1e3a5f'>Résumé exécutif</h3>
            <p style='font-size:13px;line-height:1.6'>
                {meeting.summary.replace("**","").replace("*","").replace(chr(10),"<br>")}
            </p>

            <h3 style='color:#1e3a5f'>Décisions prises</h3>
            <ul style='font-size:13px'>{decisions_html}</ul>

            <h3 style='color:#1e3a5f'>Plan d'action</h3>
            <table style='width:100%;border-collapse:collapse;font-size:13px'>
                <thead>
                    <tr style='background:#1e3a5f;color:white'>
                        <th style='padding:8px 10px;text-align:left'>Tâche</th>
                        <th style='padding:8px 10px;text-align:left'>Responsable</th>
                        <th style='padding:8px 10px;text-align:left'>Deadline</th>
                    </tr>
                </thead>
                <tbody>{tasks_html}</tbody>
            </table>

            <h3 style='color:#1e3a5f'>Prochain meeting</h3>
            <p style='background:#eaf3e0;border:1px solid #7cb97c;border-radius:6px;
                      padding:10px;color:#2d6a2d;font-weight:500'>
                📅 {meeting.next_meeting or 'Non défini'}
            </p>
        </div>

        <div style='text-align:center;font-size:11px;color:#aaa;padding:12px'>
            Meeting Summarizer — généré automatiquement par IA
        </div>
    </body></html>
    """

    msg.attach(MIMEText(body, "html"))

    # ── Pièce jointe PDF ──
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename=compte_rendu_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        msg.attach(part)

    # ── Envoi ──
    try:
        print(f"[Mailer] Connexion à {smtp_host}:{smtp_port}...")
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, receiver, msg.as_string())
        print(f"[Mailer] Email envoyé à {receiver} ✓")
        return True
    except Exception as e:
        print(f"[Mailer] Erreur : {e}")
        return False
    

    