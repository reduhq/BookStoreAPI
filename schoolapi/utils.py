from datetime import timedelta
from datetime import datetime
import logging

from jose import jwt

import smtplib

import emails
from emails.template import JinjaTemplate
from pydantic import EmailStr

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

async def send_reset_password_email(email_to:EmailStr, email:str, token:str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(f"{settings.EMAIL_TEMPLATES_DIR}/reset_password.html") as f:
        template_html = f.read()
    link = f"{settings.SERVER_HOST}/reset-password?token={token}"
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_html,
        enviroment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link
        }
    )

async def generate_password_reset_token(email:EmailStr):
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encode_jwt = jwt.encode(
        {
            "exp": exp,
            "nbf": now,
            "sub": email
        },
        key=settings.SECRET_KEY, 
        algorithm="HS256" 
    )
    return encode_jwt