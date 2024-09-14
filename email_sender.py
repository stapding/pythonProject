import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_error_email(error_message):
    sender_email = "Да"
    receiver_email = "Да"
    password = "Да"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Ошибка в приложении"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Произошла ошибка:\n\n{error_message}"
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 535) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        print(f"Не удалось отправить email: {e}")
