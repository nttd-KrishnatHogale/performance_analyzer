from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFGenerator:

    def generate(self, report, output_path):

        doc = SimpleDocTemplate(str(output_path))

        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph("<b>Performance RCA Report</b>", styles["Heading1"]))

        elements.append(Paragraph(report.get("summary", "No summary generated"), styles["Normal"]))

        elements.append(Paragraph("<b>Root Cause</b>", styles["Heading2"]))

        elements.append(Paragraph(report.get("root_cause", "Not available"), styles["Normal"]))

        elements.append(Paragraph("<b>Timeline</b>", styles["Heading2"]))

        elements.append(Paragraph(report.get("timeline", "Not available"), styles["Normal"]))

        # elements.append(Paragraph("<b>Bottlenecks</b>", styles["Heading2"]))

        # for item in report["bottlenecks"]:
        #     elements.append(
        #         Paragraph(f"• {item}", styles["Normal"])
        #     )

        # elements.append(Paragraph("<b>Recommendations</b>", styles["Heading2"]))

        # for item in report["recommendations"]:
        #     elements.append(
        #         Paragraph(f"• {item}", styles["Normal"])
        #     )
        elements.append(Paragraph("<b>Bottlenecks</b>", styles["Heading2"]))

        for item in report.get("bottlenecks", []):
            elements.append(Paragraph(f"• {item}", styles["Normal"]))

        elements.append(Paragraph("<b>Recommendations</b>", styles["Heading2"]))

        for item in report.get("recommendations", []):
            elements.append(Paragraph(f"• {item}", styles["Normal"]))

        doc.build(elements)