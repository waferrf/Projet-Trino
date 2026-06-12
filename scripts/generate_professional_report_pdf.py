from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "RAPPORT_PROJET.md"
OUTPUT = PROJECT_ROOT / "RAPPORT_PROJET_COMPLET_PROFESSIONNEL.pdf"


PRIMARY = colors.HexColor("#0f766e")
PRIMARY_DARK = colors.HexColor("#134e4a")
TEXT = colors.HexColor("#111827")
MUTED = colors.HexColor("#4b5563")
LIGHT_BG = colors.HexColor("#f8fafc")
TABLE_HEAD = colors.HexColor("#e0f2f1")
CODE_BG = colors.HexColor("#f3f4f6")
GRID = colors.HexColor("#cbd5e1")


class ArchitectureDiagram(Flowable):
    def __init__(self, width: float = 16.8 * cm, height: float = 8.8 * cm):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, avail_width, avail_height):
        self.width = min(self.width, avail_width)
        return self.width, self.height

    def _box(self, canvas, x, y, w, h, title, subtitle, fill):
        canvas.setFillColor(fill)
        canvas.setStrokeColor(colors.HexColor("#94a3b8"))
        canvas.roundRect(x, y, w, h, 7, fill=1, stroke=1)
        canvas.setFillColor(colors.white if fill != colors.white else TEXT)
        canvas.setFont("Helvetica-Bold", 8.5)
        canvas.drawCentredString(x + w / 2, y + h - 13, title)
        canvas.setFont("Helvetica", 7)
        canvas.drawCentredString(x + w / 2, y + 10, subtitle)

    def _arrow(self, canvas, x1, y1, x2, y2):
        canvas.setStrokeColor(PRIMARY_DARK)
        canvas.setLineWidth(1.2)
        canvas.line(x1, y1, x2, y2)
        angle = 0
        if abs(x2 - x1) > abs(y2 - y1):
            angle = 0 if x2 > x1 else 180
        else:
            angle = 90 if y2 > y1 else -90
        size = 5
        canvas.saveState()
        canvas.translate(x2, y2)
        canvas.rotate(angle)
        path = canvas.beginPath()
        path.moveTo(0, 0)
        path.lineTo(-size, size / 2)
        path.lineTo(-size, -size / 2)
        path.close()
        canvas.setFillColor(PRIMARY_DARK)
        canvas.drawPath(path, fill=1, stroke=0)
        canvas.restoreState()

    def draw(self):
        c = self.canv
        c.saveState()

        c.setFillColor(colors.HexColor("#f8fafc"))
        c.setStrokeColor(colors.HexColor("#d1d5db"))
        c.roundRect(0, 0, self.width, self.height, 10, fill=1, stroke=1)

        c.setFillColor(PRIMARY_DARK)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(self.width / 2, self.height - 18, "Architecture globale de la solution")

        box_w = 3.05 * cm
        box_h = 1.35 * cm
        gap_x = 0.82 * cm
        y_top = self.height - 2.45 * cm
        y_mid = self.height - 4.55 * cm
        y_low = self.height - 6.65 * cm

        x0 = 0.65 * cm
        x1 = x0 + box_w + gap_x
        x2 = x1 + box_w + gap_x
        x3 = x2 + box_w + gap_x
        x4 = x3 + box_w + gap_x

        self._box(c, x0, y_top, box_w, box_h, "CSV ventes", "Data Lakehouse", colors.HexColor("#2563eb"))
        self._box(c, x1, y_top, box_w, box_h, "MinIO", "Stockage objet", colors.HexColor("#0891b2"))
        self._box(c, x2, y_top, box_w, box_h, "Hive Metastore", "Metadonnees", colors.HexColor("#0f766e"))
        self._box(c, x3, y_top, box_w, box_h, "Apache Iceberg", "Tables lakehouse", colors.HexColor("#059669"))
        self._box(c, x4, y_top, box_w, box_h, "Trino", "SQL federe", colors.HexColor("#7c3aed"))

        self._box(c, x0, y_mid, box_w, box_h, "CSV produits", "Dataset Power BI", colors.HexColor("#ea580c"))
        self._box(c, x1, y_mid, box_w, box_h, "ClickHouse", "Base colonne", colors.HexColor("#ca8a04"))
        self._box(c, x4, y_mid, box_w, box_h, "Streamlit", "Interface data", colors.HexColor("#dc2626"))

        self._box(c, x3, y_low, box_w, box_h, "Ollama", "LLM local", colors.HexColor("#334155"))
        self._box(c, x4, y_low, box_w, box_h, "Power BI", "Dashboard", colors.HexColor("#b45309"))

        mid = box_h / 2
        self._arrow(c, x0 + box_w, y_top + mid, x1, y_top + mid)
        self._arrow(c, x1 + box_w, y_top + mid, x2, y_top + mid)
        self._arrow(c, x2 + box_w, y_top + mid, x3, y_top + mid)
        self._arrow(c, x3 + box_w, y_top + mid, x4, y_top + mid)
        self._arrow(c, x0 + box_w, y_mid + mid, x1, y_mid + mid)
        self._arrow(c, x1 + box_w, y_mid + mid, x4, y_top + 5)
        self._arrow(c, x4 + box_w / 2, y_top, x4 + box_w / 2, y_mid + box_h)
        self._arrow(c, x3 + box_w / 2, y_low + box_h, x4, y_mid + 5)
        self._arrow(c, x1 + box_w, y_mid + mid, x4, y_low + mid)

        c.restoreState()


def clean_inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font name='Helvetica-Bold'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=26,
            textColor=PRIMARY_DARK,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=PRIMARY_DARK,
            spaceBefore=12,
            spaceAfter=7,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.6,
            leading=13.4,
            textColor=TEXT,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=12.8,
            leftIndent=14,
            firstLineIndent=-8,
            textColor=TEXT,
            spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.5,
            leading=9.5,
            textColor=colors.HexColor("#1f2937"),
            backColor=CODE_BG,
            borderPadding=6,
            leftIndent=4,
            rightIndent=4,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "caption": ParagraphStyle(
            "Caption",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            leading=11,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
    }


def table_from_markdown(rows: list[str], styles: dict) -> Table:
    data = []
    for row in rows:
        if row.strip().startswith("|---"):
            continue
        cells = [clean_inline(cell.strip()) for cell in row.strip().strip("|").split("|")]
        data.append([Paragraph(cell, styles["body"]) for cell in cells])

    table = Table(data, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
                ("TEXTCOLOR", (0, 0), (-1, 0), PRIMARY_DARK),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.45, GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def parse_markdown(text: str, styles: dict) -> list:
    story = []
    lines = text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 4))
            i += 1
            continue

        if stripped.startswith("```mermaid"):
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            i += 1
            story.append(Spacer(1, 5))
            story.append(ArchitectureDiagram())
            story.append(Paragraph("Schema de l'architecture globale du projet.", styles["caption"]))
            continue

        if stripped.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            story.append(Preformatted("\n".join(code_lines), styles["code"]))
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_rows.append(lines[i])
                i += 1
            story.append(table_from_markdown(table_rows, styles))
            story.append(Spacer(1, 8))
            continue

        if stripped.startswith("# "):
            title = stripped[2:].strip()
            story.append(Paragraph(clean_inline(title), styles["title"]))
            story.append(HRFlowable(width="100%", thickness=1.1, color=PRIMARY, spaceBefore=2, spaceAfter=16))
            i += 1
            continue

        if stripped.startswith("## "):
            title = stripped[3:].strip()
            heading = Paragraph(clean_inline(title), styles["h2"])
            story.append(KeepTogether([heading, HRFlowable(width="32%", thickness=1, color=PRIMARY, spaceAfter=5)]))
            i += 1
            continue

        if stripped.startswith("- "):
            story.append(Paragraph(clean_inline(stripped), styles["bullet"]))
            i += 1
            continue

        numbered = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if numbered:
            story.append(Paragraph(clean_inline(stripped), styles["bullet"]))
            i += 1
            continue

        story.append(Paragraph(clean_inline(stripped), styles["body"]))
        i += 1

    return story


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#e5e7eb"))
    canvas.line(doc.leftMargin, 1.35 * cm, A4[0] - doc.rightMargin, 1.35 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 1.0 * cm, "Projet Trino Data Lakehouse + GenAI")
    page = f"Page {doc.page}"
    canvas.drawRightString(A4[0] - doc.rightMargin, 1.0 * cm, page)
    canvas.restoreState()


def main() -> None:
    styles = make_styles()
    markdown = SOURCE.read_text(encoding="utf-8")
    story = parse_markdown(markdown, styles)

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=1.55 * cm,
        leftMargin=1.55 * cm,
        topMargin=1.55 * cm,
        bottomMargin=1.7 * cm,
        title="Rapport Projet Data Lakehouse Trino GenAI",
        author="Projet Trino",
        pageCompression=0,
    )
    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
