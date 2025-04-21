from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

app = Flask(__name__)

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    message = Mail(
        from_email="jan.jordan@email.cz",
        to_emails=data["to"],
        subject=data["subject"],
        plain_text_content=data["message"]
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
