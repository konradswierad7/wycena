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
            "street": request.form.get("street", ""),
            "city": request.form.get("city", ""),
            "postal_code": request.form.get("postal_code", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "pump_model": request.form.get("pump_model", ""),
            "power": request.form.get("power", ""),
            "all_in_one": "tak" if request.form.get("all_in_one") else "nie",
            "kit_number": request.form.get("kit_number", ""),
            "wifi_adapter": request.form.get("wifi_adapter"),
            "water_tank": request.form.get("water_tank", ""),
            "heat_buffer": request.form.get("heat_buffer", ""),
            "price_brutto": request.form.get("price_brutto") or str(round(float(request.form.get("price_netto", 0)) * 1.08, 2))
        }

        # Validate form data
        required_fields = ["client_name", "street", "city", "postal_code", "email", "phone", 
                         "pump_model", "power", "water_tank"]
        if not all(form_data.get(field) for field in required_fields):
            flash("Proszę wypełnić wszystkie wymagane pola formularza", "error")
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)