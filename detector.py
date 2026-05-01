import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

# ===== CONFIGURE YOUR EMAIL SETTINGS =====
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 's.m.sakthivelofficial@gmail.com'      # YOUR GMAIL
SENDER_PASSWORD = 'yrknxpsacnxjamyu'                  # APP PASSWORD
RECEIVER_EMAIL = 'sakthivelsm.ai@gmail.com'           # WHERE REPORTS GO
# =========================================

def send_email_report(image_path, lat, lon, report_time, description):
    """
    Sends an email with the image, location, time and description.
    Returns True if successful, False otherwise.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f'Civic Issue Report - {report_time}'

        # Email body (HTML)
        body = f"""
        <h2>New Citizen Report via CivicEye</h2>
        <p><strong>📍 Location:</strong><br>
        Latitude: {lat}<br>
        Longitude: {lon}<br>
        <a href="https://www.google.com/maps?q={lat},{lon}">View on Map</a>
        </p>
        <p><strong>🕒 Date & Time:</strong> {report_time}</p>
        <p><strong>📝 Description:</strong><br> {description if description else 'No description provided'}</p>
        <p><em>This is an automated complaint from the CivicEye citizen portal.</em></p>
        """
        msg.attach(MIMEText(body, 'html'))

        # Attach image if it exists
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img = MIMEImage(f.read(), name=os.path.basename(image_path))
                msg.attach(img)

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
        return True

    except Exception as e:
        print("❌ Email sending failed:", e)
        return False