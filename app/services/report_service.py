from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# folders
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
REPORTS_DIR = BASE_DIR / "reports"
CHARTS_DIR = BASE_DIR / "reports/charts"

# ensure dirs exist
REPORTS_DIR.mkdir(exist_ok=True)
CHARTS_DIR.mkdir(exist_ok=True)

class ReportService:
    """
    Handles generation of PDF reports (weekly, monthly, custom).
    Uses:
        - Jinja2 templates for HTML
        - WeasyPrint for PDF conversion
        - Matplotlib for charts
    """

    @staticmethod
    def create_bar_chart(df: pd.DataFrame, x_field: str, y_field: str, out_name: str):
        """
        Creates a bar chart from a dataframe.
        Example usage:
            df = pd.DataFrame({"CourseName": [...], "AverageGPA": [...]})
            ReportService.create_bar_chart(df, "CourseName", "AverageGPA", "gpa_chart.png")
        """

        out_path = CHARTS_DIR / out_name

        plt.figure()
        plt.bar(df[x_field], df[y_field])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()

        return out_path

    @staticmethod
    def generate_pdf(template_name: str, context: dict, output_name: str):
        """
        Renders HTML template and exports it as a PDF.
        """

        template_path = TEMPLATES_DIR
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template(template_name)

        html_rendered = template.render(**context)

        output_path = REPORTS_DIR / output_name
        HTML(string=html_rendered, base_url=str(TEMPLATES_DIR)).write_pdf(output_path)

        return output_path

    @staticmethod
    def weekly_gpa_report(df: pd.DataFrame):
        """
        Complete pipeline:
        1. Generate chart
        2. Prepare context
        3. Render PDF using template 'weekly_report.html'
        """

        chart_path = ReportService.create_bar_chart(
            df,
            x_field="CourseName",
            y_field="AverageGPA",
            out_name="weekly_gpa_chart.png"
        )

        context = {
            "title": "Weekly GPA Report",
            "chart_url": str(chart_path),
            "table": df.to_dict(orient="records")
        }

        return ReportService.generate_pdf(
            template_name="weekly_report.html",
            context=context,
            output_name="weekly_gpa_report.pdf"
        )
