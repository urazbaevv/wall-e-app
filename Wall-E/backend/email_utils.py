import smtplib
from email.mime.text import MIMEText

# 📌 Email sozlamalari
SMTP_SERVER = "smtp.gmail.com"  # GMail SMTP serveri
SMTP_PORT = 587
EMAIL_SENDER = "orazbaevqudaybergen0@gmail.com"  # O‘zingizning email manzilingiz
EMAIL_PASSWORD = "jwig ssky uiuy djli"  # Gmail App Password (2FA bo‘lsa)

def send_email_notification(subject, body, recipient):
    """📧 Email orqali xabar yuborish."""
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient

    try:
        # 📌 SMTP serverga ulanib, email jo‘natish
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Xavfsiz ulanishni yoqish
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        server.quit()
        print(f"✅ Email muvaffaqiyatli yuborildi: {recipient}")
    except Exception as e:
        print(f"❌ Email yuborishda xatolik: {e}")
