from email.message import EmailMessage

from aiosmtplib import SMTP
from pydantic import EmailStr

from src.config import settings


async def send_email(recipient: EmailStr, subject: str, content: str):
    message = EmailMessage()
    message.set_content(content)
    message['Subject'] = subject
    message['From'] = settings.SMTP_USER
    message['To'] = recipient

    try:
        async with SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp_server:
            await smtp_server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            await smtp_server.send_message(message)
        print('Email sent successfully')
    except Exception as e:
        print('Error: ', str(e))


async def sending_email_with_invite_code(email: EmailStr, invite_code: str):
    subject = 'Ваш инвайт код'
    content = f'Ваш инвайт код: {invite_code}'
    # await send_email(email, subject, content)
    print(f'Отправлена почта на {email}')


async def sending_email_with_invite_link(email: EmailStr, invite_link: str):
    subject = 'Приглашение'
    content = f'Ваша ссылка приглашение: {invite_link}'
    await send_email(email, subject, content)
