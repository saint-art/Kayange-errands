from flask import Flask, request, render_template, redirect, url_for, flash
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for flashing messages

# Environment variables for SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")  # Verified sender email

@app.route('/')
def index():
    return render_template('request.html')  # Flask will look inside templates/

@app.route('/submit', methods=['POST'])
def submit_errand():
    name = request.form.get('name')
    phone = request.form.get('phone')
    errand_type = request.form.get('errand_type')
    description = request.form.get('description')

    # Send confirmation email if API key exists
    if SENDGRID_API_KEY and EMAIL_SENDER:
        try:
            message = Mail(
                from_email=EMAIL_SENDER,
                to_emails=EMAIL_SENDER,
                subject=f"New Errand Request from {name}",
                html_content=f"""
                <strong>Name:</strong> {name}<br>
                <strong>Phone:</strong> {phone}<br>
                <strong>Errand Type:</strong> {errand_type}<br>
                <strong>Description:</strong> {description}
                """
            )
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(message)
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("Error sending email, but request saved.", "error")
            return redirect(url_for('index'))

    flash("Errand request submitted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Use Render's dynamic PORT or fallback to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
