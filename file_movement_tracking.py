import os
import smtplib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Klasör yolu (Folder path)
folder_path = "/path/to/your/folder"

# Müzik ve resim dosyaları (Music and image files)
music_extensions = [".mp3", ".wav", ".flac"]
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

# E-posta ayarları (Email settings)
email_sender = "your_email@example.com"
email_receiver = "receiver_email@example.com"
email_password = "your_email_password"
smtp_server = "smtp.example.com"  # Örneğin, Gmail için "smtp.gmail.com" (For gmail)
smtp_port = 587  # Gmail için 587 (For gmail)

# E-posta gönderme fonksiyonu (Email sending function)
def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Güvenli bağlantı
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, msg.as_string())
            print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"E-posta gönderilemedi: {e}")

# Dosya değişikliklerini izleyen sınıf (Class monitoring file changes)
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        message = f"Yeni bir dosya '{event.src_path}' oluşturuldu."
        print(message)
        send_email("Dosya Oluşturuldu", message)

    def on_deleted(self, event):
        if event.is_directory:
            return
        message = f"Dosya silindi: '{event.src_path}'"
        print(message)
        send_email("Dosya Silindi", message)

    def on_moved(self, event):
        if event.is_directory:
            return
        message = f"Dosya taşındı: '{event.src_path}' -> '{event.dest_path}'"
        print(message)
        send_email("Dosya Taşındı", message)

    def on_modified(self, event):
        if event.is_directory:
            return
        message = f"Dosya güncellendi: '{event.src_path}'"
        print(message)
        send_email("Dosya Güncellendi", message)

# İzleyici başlat (Start tracker)
event_handler = FileHandler()
observer = Observer()
observer.schedule(event_handler, folder_path, recursive=False)
observer.start()

print(f"{folder_path} klasörü izleniyor...")

try:
    while True:
        pass  # Sonsuza kadar bekle (Wait forever)
except KeyboardInterrupt:
    observer.stop()

observer.join()
