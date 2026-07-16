from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
import os


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontSize=20,
        leading=24,
        alignment=1,  # center
        spaceAfter=6,
        textColor=colors.HexColor("#1a1a2e")
    ))

    styles.add(ParagraphStyle(
        name="ScoreBanner",
        fontSize=16,
        leading=20,
        alignment=1,
        spaceAfter=16,
        textColor=colors.white,
        backColor=colors.HexColor("#2e5090"),
        borderPadding=10
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        fontSize=14,
        leading=18,
        spaceBefore=14,
        spaceAfter=8,
        textColor=colors.HexColor("#2e5090"),
        fontName="Helvetica-Bold"
    ))

    styles.add(ParagraphStyle(
        name="BodyTextCustom",
        fontSize=10.5,
        leading=15,
        spaceAfter=8
    ))

    return styles


def _metrics_table(data_dict, styles):
    """Builds a two-column key/value table from a dict."""
    table_data = [["Metric", "Value"]]
    for key, value in data_dict.items():
        label = key.replace("_", " ").title()
        table_data.append([label, str(value)])

    table = Table(table_data, colWidths=[2.8 * inch, 2.8 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e5090")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5fa")]),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return table


def _bullet_list(items, styles):
    story = []
    for item in items:
        story.append(Paragraph(f"&bull;&nbsp;&nbsp;{item}", styles["BodyTextCustom"]))
    return story


def generate_report(
    candidate_name,
    question,
    transcript,
    communication_metrics,
    technical_metrics,
    star_evaluation,
    ai_feedback,
    final_score,
    output_path
):
    """
    Builds the full MirrorMind interview report PDF.

    candidate_name: str or None
    question: str
    transcript: str
    communication_metrics: dict (emotion_summary, eye_contact_pct, wpm, filler_count, pause_count, answer_duration, ...)
    technical_metrics: dict (similarity_pct, keyword_coverage_pct, technical_score, missing_keywords, ...)
    star_evaluation: dict or None (only included if not None)
    ai_feedback: dict (strengths, weaknesses, suggestions, final_summary)
    final_score: float
    output_path: str — where to save the PDF
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    styles = _build_styles()
    story = []

    # ---------------- Title ----------------
    story.append(Paragraph("MirrorMind — Interview Report", styles["ReportTitle"]))
    if candidate_name:
        story.append(Paragraph(f"Candidate: {candidate_name}", styles["BodyTextCustom"]))
    story.append(Spacer(1, 6))

    # ---------------- Final Score Banner (prominent, near top) ----------------
    story.append(Paragraph(f"Overall Score: {final_score}%", styles["ScoreBanner"]))
    story.append(Spacer(1, 10))

    # ---------------- Interview Question ----------------
    story.append(Paragraph("Interview Question", styles["SectionHeading"]))
    story.append(Paragraph(question, styles["BodyTextCustom"]))

    # ---------------- Transcript ----------------
    story.append(Paragraph("Candidate's Transcript", styles["SectionHeading"]))
    story.append(Paragraph(transcript if transcript else "No transcript recorded.", styles["BodyTextCustom"]))

    # ---------------- Communication Metrics ----------------
    story.append(Paragraph("Communication Metrics", styles["SectionHeading"]))
    story.append(_metrics_table(communication_metrics, styles))
    story.append(Spacer(1, 10))

    # ---------------- Technical Metrics ----------------
    story.append(Paragraph("Technical Metrics", styles["SectionHeading"]))
    tech_display = {k: v for k, v in technical_metrics.items() if k != "missing_keywords" and k != "matched_keywords"}
    story.append(_metrics_table(tech_display, styles))

    if technical_metrics.get("missing_keywords"):
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            f"<b>Missing Keywords:</b> {', '.join(technical_metrics['missing_keywords'])}",
            styles["BodyTextCustom"]
        ))
    if technical_metrics.get("matched_keywords"):
        story.append(Paragraph(
            f"<b>Matched Keywords:</b> {', '.join(technical_metrics['matched_keywords'])}",
            styles["BodyTextCustom"]
        ))

    # ---------------- STAR Evaluation (only if applicable) ----------------
    if star_evaluation is not None:
        story.append(Paragraph("STAR Framework Evaluation", styles["SectionHeading"]))

        star_table_data = [
            ["Situation", "Present" if star_evaluation.get("situation") else "Missing"],
            ["Task", "Present" if star_evaluation.get("task") else "Missing"],
            ["Action", "Present" if star_evaluation.get("action") else "Missing"],
            ["Result", "Present" if star_evaluation.get("result") else "Missing"],
        ]
        star_table = Table(star_table_data, colWidths=[2.8 * inch, 2.8 * inch])
        star_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f5f5fa")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
        story.append(star_table)
        story.append(Spacer(1, 8))

        if star_evaluation.get("missing"):
            story.append(Paragraph(
                f"<b>Missing Components:</b> {', '.join(star_evaluation['missing'])}",
                styles["BodyTextCustom"]
            ))

        if star_evaluation.get("suggestions"):
            story.append(Paragraph("<b>Suggestions:</b>", styles["BodyTextCustom"]))
            story.extend(_bullet_list(star_evaluation["suggestions"], styles))

    # ---------------- AI Feedback ----------------
    story.append(Paragraph("AI Feedback", styles["SectionHeading"]))

    story.append(Paragraph("<b>Strengths</b>", styles["BodyTextCustom"]))
    story.extend(_bullet_list(ai_feedback.get("strengths", []), styles))

    story.append(Paragraph("<b>Weaknesses</b>", styles["BodyTextCustom"]))
    story.extend(_bullet_list(ai_feedback.get("weaknesses", []), styles))

    story.append(Paragraph("<b>Suggestions</b>", styles["BodyTextCustom"]))
    story.extend(_bullet_list(ai_feedback.get("suggestions", []), styles))

    story.append(Paragraph("<b>Summary</b>", styles["BodyTextCustom"]))
    story.append(Paragraph(ai_feedback.get("final_summary", ""), styles["BodyTextCustom"]))

    # ---------------- Build PDF ----------------
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch
    )
    doc.build(story)

    return output_path