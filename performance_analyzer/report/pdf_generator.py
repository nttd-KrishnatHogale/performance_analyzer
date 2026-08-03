from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    def generate(self, report, output_path):

        doc = SimpleDocTemplate(str(output_path))

        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph("<b>Performance RCA Report</b>", styles["Heading1"]))

        elements.append(Paragraph(report["summary"], styles["Normal"]))

        elements.append(Paragraph("<b>Root Cause</b>", styles["Heading2"]))

        elements.append(Paragraph(report["root_cause"], styles["Normal"]))

        elements.append(Paragraph("<b>Timeline</b>", styles["Heading2"]))

        elements.append(Paragraph(report["timeline"], styles["Normal"]))

        elements.append(Paragraph("<b>Bottlenecks</b>", styles["Heading2"]))

        for item in report["bottlenecks"]:
            elements.append(
                Paragraph(f"• {item}", styles["Normal"])
            )

        elements.append(Paragraph("<b>Recommendations</b>", styles["Heading2"]))

        for item in report["recommendations"]:
            elements.append(
                Paragraph(f"• {item}", styles["Normal"])
            )

        doc.build(elements)