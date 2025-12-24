import io
from google.cloud import vision
from google.oauth2 import service_account
from datetime import datetime
import re
from ..schemas.invoice_schemas import InvoiceOCRResponse, DocumentType


class OCRService:
    def __init__(self):
        # You will place your service_account_token.json in the core folder
        # For Render, you would use an Environment Variable instead
        self.client = vision.ImageAnnotatorClient()

    async def process_invoice(self, file_content: bytes) -> InvoiceOCRResponse:
        """
        Processes image using Google Cloud Vision API (much more accurate for Hebrew).
        """
        image = vision.Image(content=file_content)

        # Performs text detection on the image file
        response = self.client.text_detection(image=image)
        texts = response.text_annotations

        if not texts:
            raise Exception("No text detected in the image")

        # The first element contains the entire text block
        full_text = texts[0].description
        return self._parse_text_to_schema(full_text)

    def _parse_text_to_schema(self, text: str) -> InvoiceOCRResponse:
        # Regex for Israeli formats (Amounts, VAT ID, Dates)
        amount_pattern = r"(\d+\.\d{2})"
        vat_id_pattern = r"(\d{9})"
        date_pattern = r"(\d{2}/\d{2}/\d{4}|\d{2}\.\d{2}\.\d{4})"

        amounts = re.findall(amount_pattern, text)
        vat_ids = re.findall(vat_id_pattern, text)
        dates = re.findall(date_pattern, text)

        total_amount = float(amounts[-1]) if amounts else 0.0  # Often total is the last amount
        amount_before_vat = round(total_amount / 1.17, 2)

        doc_type = DocumentType.INVOICE if "חשבונית" in text else DocumentType.RECEIPT

        return InvoiceOCRResponse(
            document_type=doc_type,
            business_name=text.split('\n')[0],  # Usually business name is the first line
            business_vat_number=vat_ids[0] if vat_ids else "Unknown",
            amount_before_vat=amount_before_vat,
            amount_after_vat=total_amount,
            transaction_date=self._parse_date(dates[0]) if dates else datetime.now().date(),
            invoice_number=None,
            service_description="Processed via Google Vision API"
        )

    def _parse_date(self, date_str: str):
        for fmt in ('%d/%m/%Y', '%d.%m.%Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        return datetime.now().date()