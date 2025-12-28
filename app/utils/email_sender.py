"""Email sending utility."""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import get_settings

settings = get_settings()


async def send_email(to: str, subject: str, body: str, is_html: bool = False):
    """Send email asynchronously."""
    if not settings.SMTP_USER:
        print(f"Email disabled. Would send to {to}: {subject}")
        return

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html" if is_html else "plain"))

    async with aiosmtplib.SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
        await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        await smtp.send_message(msg)
