import logging

import smtplib

import emails
from emails.template import JinjaTemplate

from schoolapi.core.config import settings

async def send_email(
    email_to:str,
    subject_template:str = "",
    html_template:str = "",
    enviroment:dict[str, str] = {}
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
        mail_to=email_to,
        html=JinjaTemplate(html_template)
    )
    message.render(**enviroment)

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        if settings.SMTP_TLS: server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAILS_FROM_EMAIL, email_to, message.as_string())
    logging.info(f"The email has been sent")

async def send_new_account_email(email_to:str, username:str, password:str) -> None:
    project_name:str = settings.PROJECT_NAME
    subject:str = f"{project_name} - New account for user {username}"
    with open (f"{settings.EMAIL_TEMPLATES_DIR}/new_account.html") as f:
        template_str:str = f.read()
    link = settings.SERVER_HOST
    await send_email(
        email_to= email_to,
        subject_template= subject,
        html_template= template_str,
        enviroment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email_to": email_to,
            "link": link
        }
    )