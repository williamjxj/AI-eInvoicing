"""
Document Reader - First capability: READ
Extracts content from various financial document formats using open-source tools
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

try:
    import PyPDF2
    from PIL import Image
    import pytesseract
except ImportError:
    # Graceful degradation for missing dependencies
    PyPDF2 = None
    Image = None
    pytesseract = None

logger = logging.getLogger(__name__)


class DocumentReader:
    """
    Reads and extracts content from financial documents
    Supports: PDF, images (PNG, JPG, TIFF), and other formats
    Uses open-source OCR and parsing libraries
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize document reader with configuration
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.tif', '.txt']
        logger.info("DocumentReader initialized with open-source stack")
    
    def read_document(self, file_path: str) -> Dict[str, Any]:
        """
        Read and extract content from a document
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        file_ext = path.suffix.lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported format: {file_ext}")
        
        logger.info(f"Reading document: {file_path}")
        
        if file_ext == '.pdf':
            return self._read_pdf(path)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.tif']:
            return self._read_image(path)
        elif file_ext == '.txt':
            return self._read_text(path)
        else:
            raise ValueError(f"Unsupported format: {file_ext}")
    
    def _read_pdf(self, path: Path) -> Dict[str, Any]:
        """Extract text from PDF using PyPDF2"""
        if PyPDF2 is None:
            return {
                'text': "PDF reading requires PyPDF2 library",
                'format': 'pdf',
                'pages': 0,
                'metadata': {}
            }
        
        try:
            text_content = []
            metadata = {}
            
            with open(path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                # Extract metadata
                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                    }
                
                # Extract text from all pages
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    text_content.append(text)
            
            return {
                'text': '\n\n'.join(text_content),
                'format': 'pdf',
                'pages': num_pages,
                'metadata': metadata,
                'file_name': path.name
            }
        except Exception as e:
            logger.error(f"Error reading PDF: {str(e)}")
            return {
                'text': '',
                'format': 'pdf',
                'error': str(e),
                'file_name': path.name
            }
    
    def _read_image(self, path: Path) -> Dict[str, Any]:
        """Extract text from image using OCR (pytesseract)"""
        if Image is None or pytesseract is None:
            return {
                'text': "Image reading requires Pillow and pytesseract libraries",
                'format': path.suffix,
                'metadata': {}
            }
        
        try:
            image = Image.open(path)
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            # Get image metadata
            metadata = {
                'width': image.width,
                'height': image.height,
                'mode': image.mode,
                'format': image.format,
            }
            
            return {
                'text': text,
                'format': path.suffix,
                'metadata': metadata,
                'file_name': path.name
            }
        except Exception as e:
            logger.error(f"Error reading image: {str(e)}")
            return {
                'text': '',
                'format': path.suffix,
                'error': str(e),
                'file_name': path.name
            }
    
    def _read_text(self, path: Path) -> Dict[str, Any]:
        """Read plain text file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return {
                'text': text,
                'format': 'txt',
                'metadata': {
                    'size': path.stat().st_size,
                    'encoding': 'utf-8'
                },
                'file_name': path.name
            }
        except Exception as e:
            logger.error(f"Error reading text file: {str(e)}")
            return {
                'text': '',
                'format': 'txt',
                'error': str(e),
                'file_name': path.name
            }
    
    def read_multiple(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Read multiple documents in batch
        
        Args:
            file_paths: List of document file paths
            
        Returns:
            List of dictionaries with extracted content
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.read_document(file_path)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to read {file_path}: {str(e)}")
                results.append({
                    'text': '',
                    'error': str(e),
                    'file_name': Path(file_path).name
                })
        return results
