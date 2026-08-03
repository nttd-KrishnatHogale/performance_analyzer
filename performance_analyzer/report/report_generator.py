from pathlib import Path

from performance_analyzer.report.html_generator import HTMLGenerator
from performance_analyzer.report.pdf_generator import PDFGenerator


class ReportGenerator:

    def generate(
        self,
        run_id,
        llm_report,
        timeline,
        correlations
    ):

        report_dir = Path("reports") / str(run_id)
        report_dir.mkdir(parents=True, exist_ok=True)

        html_path = report_dir / "report.html"
        pdf_path = report_dir / "report.pdf"

        HTMLGenerator().generate(
            html_path,
            llm_report,
            timeline,
            correlations
        )

        PDFGenerator().generate(
            html_path,
            pdf_path
        )

        return {
            "html": str(html_path),
            "pdf": str(pdf_path)
        }