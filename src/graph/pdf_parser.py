import os
from pypdf import PdfReader
from src.exceptions import IngestionError
from src.logger import log

class PDFParser:
    """Handles extracting and cleaning text from PDF documents."""
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extracts text from a given PDF file."""
        if not os.path.exists(file_path):
            raise IngestionError(f"File not found: {file_path}")
        
        try:
            log.info(f"Parsing PDF: {file_path}")
            reader = PdfReader(file_path)
            text = ""
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            cleaned_text = PDFParser.clean_text(text)
            log.info(f"Successfully extracted {len(cleaned_text)} characters.")
            return cleaned_text
        except Exception as e:
            raise IngestionError(f"Failed to parse PDF: {str(e)}")

    @staticmethod
    def clean_text(text: str) -> str:
        """Removes excessive whitespace and normalizes the text."""
        import re
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        return text.strip()
