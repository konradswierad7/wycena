from docx import Document
import os
import logging
from datetime import datetime

class DocumentHandler:
    def __init__(self):
        self.template_path = "template.docx"
        self.logger = logging.getLogger(__name__)

    def generate_document(self, data):
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
            output_filename = f"generated_docs/offer_{timestamp}.docx"
            
            # Ensure directory exists
            os.makedirs("generated_docs", exist_ok=True)
            
            # Save document
            doc.save(output_filename)
            return output_filename

        except Exception as e:
            self.logger.error(f"Error generating document: {str(e)}")
            raise

    def generate_preview(self, data):
        """Generate HTML preview of the document."""
        try:
            # Create a simple HTML preview
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
