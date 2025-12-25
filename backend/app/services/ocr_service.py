import re
import os
import json
from datetime import datetime
from google.cloud import vision
from google.oauth2 import service_account
from ..schemas.invoice_schemas import InvoiceOCRResponse, DocumentType


class OCRService:
    def __init__(self):
        """
        Initialize the Google Vision client by checking for Environment Variables (Production)
        or falling back to the local credentials file (Development).
        """
        # 1. Attempt to get credentials from the Render Environment Variable
        key_content = os.environ.get("GCP_SERVICE_ACCOUNT_JSON")

        if key_content:
            try:
                # Production: Load credentials from the JSON string stored in Environment Variables
                key_info = json.loads(key_content)
                credentials = service_account.Credentials.from_service_account_info(key_info)
                self.client = vision.ImageAnnotatorClient(credentials=credentials)
            except Exception as e:
                print(f"Error loading credentials from Environment Variable: {e}")
                # Fallback to default behavior if parsing fails
                self.client = vision.ImageAnnotatorClient()
        else:
            # Development: Uses the local 'google-key.json' file via GOOGLE_APPLICATION_CREDENTIALS
            # Make sure your local .env has: GOOGLE_APPLICATION_CREDENTIALS="google-key.json"
            self.client = vision.ImageAnnotatorClient()

    async def process_invoice(self, file_content: bytes) -> InvoiceOCRResponse:
        """
        Processes image content using Google Vision with improved parsing.
        """
        image = vision.Image(content=file_content)
        response = self.client.text_detection(image=image)
        annotations = response.text_annotations

        if not annotations:
            raise Exception("No text detected in the image")

        full_text = annotations[0].description
        return self._parse_text_to_schema(full_text)

    def _parse_text_to_schema(self, text: str) -> InvoiceOCRResponse:
        # Split into lines and clean whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # 1. ENHANCED Price Extraction - Multiple Patterns
        found_prices = []

        # Pattern 1: Standard decimal with dot (123.45)
        pattern1 = r'\b(\d{1,6}\.\d{2})\b'
        found_prices.extend(re.findall(pattern1, text))

        # Pattern 2: Israeli format with comma (123,45)
        pattern2 = r'\b(\d{1,6},\d{2})\b'
        found_prices.extend([p.replace(',', '.') for p in re.findall(pattern2, text)])

        # Pattern 3: No decimals but likely prices (look for "total", "סה״כ", etc.)
        # Multi-language receipt keywords
        total_keywords = [
            # Hebrew
            'סה״כ', 'סהכ', 'סך הכל', 'סכום', 'לתשלום', 'סה"כ',
            # English
            'total', 'amount', 'sum', 'balance', 'due', 'payment', 'grand total',
            # Other common
            'subtotal', 'net', 'gross'
        ]
        for line in lines:
            if any(keyword in line.lower() for keyword in total_keywords):
                # Extract numbers from this line
                numbers = re.findall(r'\b(\d{2,6})\b', line)
                for num in numbers:
                    # If it's a reasonable price range (20-999999)
                    if 20 <= int(num) <= 999999:
                        found_prices.append(num + '.00')

        # Pattern 4: Prices with thousand separators (1,234.56 or 1.234,56)
        pattern4 = r'\b(\d{1,3}[,\.]\d{3}[,\.]\d{2})\b'
        for match in re.findall(pattern4, text):
            # Normalize: last separator is decimal, others are thousands
            normalized = match.replace(',', '').replace('.', '')
            # Add decimal point before last 2 digits
            if len(normalized) > 2:
                normalized = normalized[:-2] + '.' + normalized[-2:]
                found_prices.append(normalized)

        total_amount = 0.0
        if found_prices:
            # Convert to floats and pick the MAX value
            float_prices = []
            for p in found_prices:
                try:
                    float_prices.append(float(p))
                except ValueError:
                    continue

            if float_prices:
                total_amount = max(float_prices)

        # Fallback: If still 0, look for ANY reasonable number in the text
        if total_amount == 0.0:
            all_numbers = re.findall(r'\b(\d+)\b', text)
            for num in all_numbers:
                val = int(num)
                # Israeli shekel typical range for business expenses
                if 10 <= val <= 50000:
                    total_amount = float(val)
                    break

        # 2. Israeli Business ID (H.P. / O.M.) - Always 9 digits
        vat_id_pattern = r'\b(\d{9})\b'
        vat_ids = re.findall(vat_id_pattern, text)
        business_id = vat_ids[0] if vat_ids else "Unknown"

        # 3. Date Extraction (Israeli format DD/MM/YYYY or DD.MM.YYYY)
        date_pattern = r'(\d{2}[/\.]\d{2}[/\.]\d{2,4})'
        dates = re.findall(date_pattern, text)

        # 4. Business Name Logic - Multi-language
        business_name = "Unknown Vendor"
        generic_terms = [
            # Hebrew
            "חשבונית", "מס", "קבלה", "נאמן", "מספר", "מקור", "תאריך", "עוסק", "ח.פ", "ע.מ",
            # English
            "TAX", "INV", "INVOICE", "RECEIPT", "DATE", "NUMBER", "NO.", "#",
            "VAT", "ID", "BUSINESS", "COMPANY"
        ]

        for line in lines[:8]:  # Look at top 8 lines (increased from 5)
            # Skip very short lines and lines with only numbers
            if len(line) < 3 or line.isdigit():
                continue
            # Skip lines that are mostly numbers
            if sum(c.isdigit() for c in line) / len(line) > 0.5:
                continue
            # Check if line contains generic terms
            if not any(term in line for term in generic_terms):
                business_name = line
                break

        # 5. Document Type Detection - Multi-language
        doc_type = DocumentType.INVOICE if any(
            word in text.lower() for word in ["חשבונית", "invoice", "tax invoice"]) else DocumentType.RECEIPT

        # Calculate Before VAT (Standard 17%)
        amount_before_vat = round(total_amount / 1.17, 2) if total_amount > 0 else 0.0

        # 6. Enhanced Invoice Number Detection - Multi-language
        invoice_number = None
        invoice_patterns = [
            # Hebrew
            r'(?:מס[\'׳]?\s*חשבונית|מספר)[:\s]*([A-Z0-9\-/]+)',
            # English
            r'(?:invoice\s*#?|inv\s*#?|receipt\s*#?|ref)[:\s]*([A-Z0-9\-/]+)',
            # Generic patterns
            r'\b([A-Z]{2,}\d{4,})\b',  # Pattern like AB12345
            r'#\s*(\d{4,})',  # Pattern like #12345
            r'NO[.:]?\s*([A-Z0-9\-/]+)',  # Pattern like NO: 12345
        ]
        for pattern in invoice_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                invoice_number = match.group(1)
                break

        return InvoiceOCRResponse(
            document_type=doc_type,
            business_name=business_name,
            business_vat_number=business_id,
            amount_before_vat=amount_before_vat,
            amount_after_vat=total_amount,
            transaction_date=self._parse_date(dates[0]) if dates else datetime.now().date(),
            invoice_number=invoice_number,
            service_description="Universal Multi-Language OCR with Israeli & International Format Support"
        )

    def _parse_date(self, date_str: str):
        # Normalize dots to slashes for parsing
        normalized_date = date_str.replace('.', '/')
        formats = ('%d/%m/%Y', '%d/%m/%y')
        for fmt in formats:
            try:
                return datetime.strptime(normalized_date, fmt).date()
            except ValueError:
                continue
        return datetime.now().date()