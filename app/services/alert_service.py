# app/services/alert_service.py

import smtplib
from email.message import EmailMessage
from app.config import settings


class AlertService:
    """
    Handles sending email notifications such as:
    - Low GPA warnings
    - Risk prediction alerts
    - Weekly report delivery
    """

    @staticmethod
    def send_email(to_email: str, subject: str, body: str, attachments: list = None):
        """
        Send an email with optional attachments.

        :param to_email: Recipient email address
        :param subject: Email subject line
        :param body: Text content of the email
        :param attachments: List of file paths to attach (PDFs, images, etc.)
        """
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_USER
        msg["To"] = to_email
        msg.set_content(body)

        # Handle file attachments
        if attachments:
            for file_path in attachments:
                try:
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        file_name = file_path.split("/")[-1]

                    msg.add_attachment(
                        file_data,
                        maintype="application",
                        subtype="octet-stream",
                        filename=file_name
                    )
                except Exception as e:
                    print(f"Failed to attach {file_path}: {e}")

        # Send email securely using SMTP SSL
        try:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
                smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                smtp.send_message(msg)
                print(f"📧 Email sent successfully to {to_email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            raise RuntimeError("Email delivery failed") from e
