from flask import Flask, request, jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import os
import base64

app = Flask(__name__)

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()
    try:
        message = Mail(
            from_email="jan.jordan@email.cz",
            to_emails=data["to"],
            subject=data["subject"],
            plain_text_content=data["message"]
        )

        if "filecontent_base64" in data and "filename" in data:
            attachment = Attachment()
            attachment.file_content = FileContent(data["filecontent_base64"])
            attachment.file_type = FileType("application/pdf")
            attachment.file_name = FileName(data["filename"])
            attachment.disposition = Disposition("attachment")
            message.attachments = [attachment]

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print("SendGrid response:", response.status_code)
        return jsonify({"status": "sent"}), 200

    except Exception as e:
        print("CHYBA V SERVERU:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)