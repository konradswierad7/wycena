from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from document_handler import DocumentHandler
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize document handler
doc_handler = DocumentHandler()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_document():
    try:
        # Get form data
        form_data = {
            "client_name": request.form.get("client_name", ""),
            "service_details": request.form.get("service_details", ""),
            "price": request.form.get("price", ""),
            "date": request.form.get("date", ""),
            "company_name": request.form.get("company_name", ""),
            "contact_person": request.form.get("contact_person", ""),
            "email": request.form.get("email", "")
        }

        # Validate form data
        if not all(form_data.values()):
            flash("Proszę wypełnić wszystkie pola formularza", "error")
            return redirect(url_for("index"))

        # Generate document
        output_filename = doc_handler.generate_document(form_data)
        
        # Send file
        return send_file(
            output_filename,
            as_attachment=True,
            download_name=f"Oferta_{form_data['client_name']}.docx"
        )

    except Exception as e:
        logger.error(f"Error generating document: {str(e)}")
        flash("Wystąpił błąd podczas generowania dokumentu", "error")
        return redirect(url_for("index"))

@app.route("/preview", methods=["POST"])
def preview_document():
    try:
        form_data = request.form.to_dict()
        preview_html = doc_handler.generate_preview(form_data)
        return render_template("preview.html", preview_content=preview_html)
    except Exception as e:
        logger.error(f"Error generating preview: {str(e)}")
        return "Błąd podczas generowania podglądu", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
