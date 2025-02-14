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
            "pump_model": request.form.get("pump_model", ""),
            "power": request.form.get("power", ""),
            "all_in_one": "tak" if request.form.get("all_in_one") else "nie",
            "water_tank": request.form.get("water_tank", ""),
            "heat_buffer": request.form.get("heat_buffer", ""),
            "price_brutto": request.form.get("price_brutto") or str(round(float(request.form.get("price_netto", 0)) * 1.08, 2))
        }

        # Validate form data
        if not all(value for key, value in form_data.items() if key != "all_in_one"):
            flash("Proszę wypełnić wszystkie wymagane pola formularza", "error")
            return redirect(url_for("index"))

        # Get output format
        output_format = request.form.get("format", "docx")

        # Generate document
        output_filename = doc_handler.generate_document(form_data, output_format)

        # Send file
        return send_file(
            output_filename,
            as_attachment=True,
            download_name=f"Oferta_{form_data['client_name']}.{output_format}"
        )

    except Exception as e:
        logger.error(f"Error generating document: {str(e)}")
        flash("Wystąpił błąd podczas generowania dokumentu", "error")
        return redirect(url_for("index"))

@app.route("/preview", methods=["POST"])
def preview_document():
    try:
        form_data = request.form.to_dict()
        if form_data.get("price_netto") and not form_data.get("price_brutto"):
            form_data["price_brutto"] = str(round(float(form_data["price_netto"]) * 1.08, 2))
        form_data["all_in_one"] = "tak" if form_data.get("all_in_one") else "nie"

        preview_html = doc_handler.generate_preview(form_data)
        return preview_html
    except Exception as e:
        logger.error(f"Error generating preview: {str(e)}")
        return "Błąd podczas generowania podglądu", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)