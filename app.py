from flask import Flask, render_template, request, redirect, flash, url_for
import base64
import os
from datetime import datetime
from detector import send_email_report

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024   # 10 MB limit

os.makedirs('static', exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html', active='home')

@app.route('/about')
def about():
    return render_template('index.html', active='about')

@app.route('/send', methods=['POST'])
def send_report():
    try:
        img_data = request.form.get('image')
        lat = request.form.get('lat', 'Not available')
        lon = request.form.get('lon', 'Not available')
        time_val = request.form.get('time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        desc = request.form.get('desc', '')

        if not img_data or not img_data.startswith('data:image'):
            flash('No image captured! Please take a photo first.', 'danger')
            return redirect(url_for('home'))

        # Decode base64 image
        img_data = img_data.split(',')[1]
        img_bytes = base64.b64decode(img_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"static/report_{timestamp}.png"
        with open(image_path, 'wb') as f:
            f.write(img_bytes)

        success = send_email_report(
            image_path=image_path,
            lat=lat,
            lon=lon,
            report_time=time_val,
            description=desc
        )

        if success:
            flash('✅ Report sent successfully to authorities!', 'success')
        else:
            flash('❌ Failed to send email. Check server logs.', 'danger')

        # Optional: delete image after sending to save space
        # os.remove(image_path)

    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        print(e)

    return redirect(url_for('home'))



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)