import os
from datetime import datetime
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        # Utilisation de .encode('latin-1', 'replace').decode('latin-1') pour les accents
        txt = "Meeting Summarizer — généré automatiquement par IA".encode('latin-1', 'replace').decode('latin-1')
        self.cell(0, 10, txt, align="C")

def generate_pdf(meeting, output_path: str = "outputs/meeting_summary.pdf") -> str:
    os.makedirs("outputs", exist_ok=True)

    # Utilisation de Helvetica qui est standard
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    effective_width = pdf.w - pdf.l_margin - pdf.r_margin 

    # ── Titre ──
    pdf.set_fill_color(30, 58, 95)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 15)
    title = "Compte-rendu de réunion".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(effective_width, 12, title, fill=True, ln=True, align="C")
    
    pdf.set_font("Helvetica", "", 9)
    date_str = f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(effective_width, 7, date_str, fill=True, ln=True, align="C")
    pdf.ln(6)

    def section_title(title):
        pdf.set_text_color(30, 58, 95)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(effective_width, 7, title.encode('latin-1', 'replace').decode('latin-1'), ln=True)
        pdf.set_draw_color(30, 58, 95)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + effective_width, pdf.get_y())
        pdf.ln(3)
        pdf.set_text_color(0, 0, 0)

    # ── Résumé ──
    section_title("RÉSUMÉ EXÉCUTIF")
    pdf.set_font("Helvetica", "", 10)
    # Nettoyage Markdown et gestion encodage
    summary_text = meeting.summary.replace("**", "").replace("*", "").replace("#", "")
    pdf.multi_cell(effective_width, 6, summary_text.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)

    # ── Décisions ──
    section_title("DÉCISIONS PRISES")
    pdf.set_font("Helvetica", "", 10)
    for d in meeting.decisions:
        clean_d = d.replace("**", "").replace("*", "")
        pdf.set_x(pdf.l_margin)
        pdf.cell(5, 6, "- ")
        pdf.multi_cell(effective_width - 5, 6, clean_d.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)

    # ── Tableau tâches ──
    section_title("PLAN D'ACTION")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(30, 58, 95)
    pdf.set_text_color(255, 255, 255)
    col = [effective_width * 0.45, effective_width * 0.30, effective_width * 0.25]
    
    # Header Tableau
    pdf.cell(col[0], 8, "Tâche".encode('latin-1', 'replace').decode('latin-1'), border=1, fill=True)
    pdf.cell(col[1], 8, "Responsable", border=1, fill=True)
    pdf.cell(col[2], 8, "Deadline", border=1, fill=True, ln=True)

    pdf.set_font("Helvetica", "", 9)
    for i, t in enumerate(meeting.tasks):
        pdf.set_text_color(0, 0, 0)
        fill = i % 2 == 0
        pdf.set_fill_color(244, 247, 251) if fill else pdf.set_fill_color(255, 255, 255)
        
        # On utilise t.title, t.owner, t.deadline (accès attributs Pydantic)
        task_name = t.title[:45].encode('latin-1', 'replace').decode('latin-1')
        owner = (t.owner or "-")[:25].encode('latin-1', 'replace').decode('latin-1')
        deadline = (t.deadline or "-")[:20].encode('latin-1', 'replace').decode('latin-1')
        
        pdf.cell(col[0], 7, task_name, border=1, fill=fill)
        pdf.cell(col[1], 7, owner, border=1, fill=fill)
        pdf.cell(col[2], 7, deadline, border=1, fill=fill, ln=True)
    pdf.ln(5)

    # ── Prochain meeting ──
    section_title("PROCHAIN MEETING")
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(45, 106, 45)
    next_m = f"-> {meeting.next_meeting or 'Non défini'}".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(effective_width, 8, next_m, ln=True)

    pdf.output(output_path)
    print(f"[PDF] Généré : {output_path}")
    return output_path