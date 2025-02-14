from docx import Document
import os
import logging
from datetime import datetime
from docx2pdf import convert

class DocumentHandler:
    def __init__(self):
        self.template_path = "attached_assets/chat.docx"
        self.logger = logging.getLogger(__name__)

    def generate_document(self, data, output_format='docx'):
        """Generate a document from template using provided data."""
        try:
            doc = Document(self.template_path)

            # Replace placeholders in paragraphs
            for paragraph in doc.paragraphs:
                self._replace_placeholders_in_paragraph(paragraph, data)

            # Replace placeholders in tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            self._replace_placeholders_in_paragraph(paragraph, data)

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs("generated_docs", exist_ok=True)
            base_filename = f"generated_docs/oferta_{timestamp}"

            # Save document as DOCX
            docx_filename = f"{base_filename}.docx"
            doc.save(docx_filename)

            if output_format == 'pdf':
                # Convert to PDF
                pdf_filename = f"{base_filename}.pdf"
                convert(docx_filename, pdf_filename)
                return pdf_filename

            return docx_filename

        except Exception as e:
            self.logger.error(f"Error generating document: {str(e)}")
            raise

    def _replace_placeholders_in_paragraph(self, paragraph, data):
        """Replace placeholders in a paragraph with actual data."""
        if not paragraph.text:
            return

        text = paragraph.text
        runs = paragraph.runs

        # Lista placeholderów do zastąpienia
        replacements = {
            "{imie_nazwisko}": data.get("client_name", ""),
            "{ulica}": data.get("street", ""),
            "{miasto}": data.get("city", ""),
            "{kod_pocztowy}": data.get("postal_code", ""),
            "{pompa_model}": data.get("pump_model", ""),
            "{moc_kw}": f"{data.get('power', '')} kW",
            "{typ_pompy}": "ALL IN ONE" if data.get("all_in_one") == "tak" else "SPLIT",
            "{zbiornik_cwu}": data.get("water_tank", ""),
            "{bufor_ciepla}": data.get("heat_buffer", ""),
            "{cena_brutto}": f"{data.get('price_brutto', '')} PLN",
            "{data}": datetime.now().strftime("%d.%m.%Y")
        }

        # Zachowaj formatowanie tekstu
        if len(runs) <= 1:
            # Jeśli paragraf ma tylko jeden run lub wcale
            for placeholder, value in replacements.items():
                if placeholder in text:
                    text = text.replace(placeholder, str(value))
            if runs:
                runs[0].text = text
            else:
                paragraph.text = text
        else:
            # Jeśli paragraf ma wiele runów, zachowaj formatowanie każdego
            for run in runs:
                for placeholder, value in replacements.items():
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, str(value))

    def generate_preview(self, data):
        """Generate HTML preview of the document."""
        try:
            preview_template = """
            <div class="preview-document">
                <div class="preview-header">
                    <h1>Oferta dla: {client_name}</h1>
                    <p>Data: {date}</p>
                </div>
                <div class="preview-content">
                    <p><strong>Adres:</strong><br>
                    {street}<br>
                    {postal_code} {city}</p>

                    <p><strong>Szczegóły techniczne:</strong><br>
                    Pompa Panasonic: {pump_model}<br>
                    Moc: {power} kW<br>
                    Typ: {all_in_one}<br>
                    Zbiornik CWU: {water_tank}<br>
                    Bufor ciepła: {heat_buffer}</p>

                    <p><strong>Cena:</strong> {price_brutto} PLN brutto</p>
                </div>
            </div>
            """

            preview_data = {
                'client_name': data.get('client_name', ''),
                'date': datetime.now().strftime("%d.%m.%Y"),
                'street': data.get('street', ''),
                'city': data.get('city', ''),
                'postal_code': data.get('postal_code', ''),
                'pump_model': data.get('pump_model', ''),
                'power': data.get('power', ''),
                'all_in_one': 'ALL IN ONE' if data.get('all_in_one') == 'tak' else 'SPLIT',
                'water_tank': data.get('water_tank', ''),
                'heat_buffer': data.get('heat_buffer', ''),
                'price_brutto': data.get('price_brutto', '')
            }

            return preview_template.format(**preview_data)

        except Exception as e:
            self.logger.error(f"Error generating preview: {str(e)}")
            raise