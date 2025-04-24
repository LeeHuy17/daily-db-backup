# File chính thực hiện backup
import os
import shutil
import smtplib
import time
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

# Load thông tin từ .env
load_dotenv()

# Cấu hình mail
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

SOURCE_FOLDER = '.'
BACKUP_FOLDER = 'backup'
os.makedirs(BACKUP_FOLDER, exist_ok=True)

def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email đã gửi thành công.")
    except Exception as e:
        print(f"❌ Gửi email thất bại: {e}")

def backup_databases():
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    success_files = []
    failed_files = []

    for file in os.listdir(SOURCE_FOLDER):
        if file.endswith('.sql') or file.endswith('.sqlite3'):
            try:
                src = os.path.join(SOURCE_FOLDER, file)
                dst = os.path.join(BACKUP_FOLDER, f"{now}_{file}")
                shutil.copy2(src, dst)
                success_files.append(file)
            except Exception as e:
                failed_files.append(f"{file}: {e}")

    if success_files:
        subject = "✅ Backup thành công"
        body = "Backup các file sau:\n" + "\n".join(success_files)
    else:
        subject = "❌ Backup thất bại"
        body = "Không thể backup file nào.\nChi tiết lỗi:\n" + "\n".join(failed_files)

    send_email(subject, body)

# Vòng lặp chạy liên tục
print("🚀 Bắt đầu theo dõi thời gian để backup lúc 00:00 mỗi ngày...")
while True:
    now = datetime.now()
    if now.hour == 0 and now.minute == 54:
        print("🕛 Đến 00:00 - Thực hiện backup...")
        backup_databases()

        # Đợi 70 giây để tránh lặp lại backup trong cùng phút
        time.sleep(70)
    else:
        # Kiểm tra mỗi phút
        time.sleep(30)
