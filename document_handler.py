from docx import Document
import os
import logging
from datetime import datetime
from docx2pdf import convert

class DocumentHandler:
    def __init__(self):
        self.template_path = "template.docx"
        self.logger = logging.getLogger(__name__)

    def generate_document(self, data, output_format='docx'):
        """Generate a document from template using provided data."""
        try:
            doc = Document(self.template_path)

            # Replace placeholders in paragraphs
            for paragraph in doc.paragraphs:
                for key, value in data.items():
                    placeholder = f"{{{key}}}"
                    if placeholder in paragraph.text:
                        paragraph.text = paragraph.text.replace(placeholder, value)

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"generated_docs/offer_{timestamp}"

            # Ensure directory exists
            os.makedirs("generated_docs", exist_ok=True)

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
                    <h2>Szczegóły usługi</h2>
                    <p>{service_details}</p>
                    <h2>Wycena</h2>
                    <p>{price} PLN</p>
                </div>
                <div class="preview-footer">
                    <p>Kontakt: {contact_person}</p>
                    <p>Email: {email}</p>
                    <p>{company_name}</p>
                </div>
            </div>
            """

            return preview_template.format(**data)

        except Exception as e:
            self.logger.error(f"Error generating preview: {str(e)}")
            raise