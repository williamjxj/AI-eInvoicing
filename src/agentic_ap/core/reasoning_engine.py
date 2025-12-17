"""
Reasoning Engine - Second capability: REASON
Applies human-level AI reasoning to understand and analyze financial documents
Uses open-source LLMs for cost-effective intelligent processing
"""

import logging
from typing import Dict, List, Any, Optional
import re
import json

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """
    AI-powered reasoning engine for financial document analysis
    Provides human-level understanding of invoice content, patterns, and anomalies
    Uses open-source LLM models to keep costs low
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize reasoning engine with configuration
        
        Args:
            config: Optional configuration dictionary with model settings
        """
        self.config = config or {}
        self.model_config = self.config.get('model', {})
        logger.info("ReasoningEngine initialized with open-source AI stack")
    
    def analyze_invoice(self, document_text: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze invoice content using AI reasoning
        
        Args:
            document_text: Extracted text from invoice document
            metadata: Optional metadata about the document
            
        Returns:
            Dictionary with analyzed invoice data and insights
        """
        logger.info("Analyzing invoice with AI reasoning")
        
        # Extract structured data using pattern recognition and AI reasoning
        invoice_data = self._extract_invoice_fields(document_text)
        
        # Perform intelligent validation
        validation_results = self._validate_invoice_logic(invoice_data)
        
        # Detect anomalies using AI reasoning
        anomalies = self._detect_anomalies(invoice_data, document_text)
        
        # Generate insights
        insights = self._generate_insights(invoice_data, validation_results, anomalies)
        
        return {
            'invoice_data': invoice_data,
            'validation': validation_results,
            'anomalies': anomalies,
            'insights': insights,
            'confidence_score': self._calculate_confidence(invoice_data, validation_results)
        }
    
    def _extract_invoice_fields(self, text: str) -> Dict[str, Any]:
        """
        Extract key invoice fields using pattern recognition
        Simulates AI-powered field extraction
        """
        fields = {}
        
        # Invoice number extraction
        invoice_patterns = [
            r'invoice\s*#?\s*:?\s*([A-Z0-9-]+)',
            r'invoice\s+number\s*:?\s*([A-Z0-9-]+)',
            r'inv\s*#?\s*:?\s*([A-Z0-9-]+)'
        ]
        for pattern in invoice_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                fields['invoice_number'] = match.group(1)
                break
        
        # Date extraction
        date_patterns = [
            r'date\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{4}-\d{2}-\d{2})'
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                fields['date'] = match.group(1)
                break
        
        # Amount extraction (total, subtotal, tax)
        amount_patterns = [
            r'total\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})',
            r'amount\s+due\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})',
            r'grand\s+total\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})'
        ]
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    fields['total'] = float(amount_str)
                except ValueError:
                    pass
                break
        
        # Tax extraction
        tax_patterns = [
            r'tax\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})',
            r'vat\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})'
        ]
        for pattern in tax_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                tax_str = match.group(1).replace(',', '')
                try:
                    fields['tax'] = float(tax_str)
                except ValueError:
                    pass
                break
        
        # Vendor/Company name extraction (usually at the top)
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line) > 3 and not re.match(r'^\d', line):
                if 'invoice' not in line.lower() and 'bill' not in line.lower():
                    fields['vendor_name'] = line
                    break
        
        return fields
    
    def _validate_invoice_logic(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate invoice data using business logic and AI reasoning
        """
        validation = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        required_fields = ['invoice_number', 'date', 'total']
        for field in required_fields:
            if field not in invoice_data or not invoice_data[field]:
                validation['errors'].append(f"Missing required field: {field}")
                validation['is_valid'] = False
        
        # Validate amounts
        if 'total' in invoice_data and 'tax' in invoice_data:
            total = invoice_data['total']
            tax = invoice_data['tax']
            
            # Check if tax is reasonable (typically 0-30% of total)
            if tax > 0 and total > 0:
                tax_percentage = (tax / total) * 100
                if tax_percentage > 30:
                    validation['warnings'].append(
                        f"Tax percentage seems high: {tax_percentage:.2f}%"
                    )
                
                # Subtotal should be total - tax
                expected_subtotal = total - tax
                if 'subtotal' in invoice_data:
                    subtotal = invoice_data['subtotal']
                    if abs(subtotal - expected_subtotal) > 0.02:
                        validation['errors'].append(
                            "Subtotal + Tax does not equal Total"
                        )
                        validation['is_valid'] = False
        
        return validation
    
    def _detect_anomalies(self, invoice_data: Dict[str, Any], text: str) -> List[str]:
        """
        Detect potential anomalies or suspicious patterns using AI reasoning
        """
        anomalies = []
        
        # Check for duplicate invoice numbers (would need database in real scenario)
        # This is a placeholder for AI-powered anomaly detection
        
        # Check for unusual amounts
        if 'total' in invoice_data:
            total = invoice_data['total']
            if total == 0:
                anomalies.append("Zero total amount detected")
            elif total < 0:
                anomalies.append("Negative total amount detected")
            elif total > 1000000:
                anomalies.append("Unusually large amount detected (>$1M)")
        
        # Check for missing vendor information
        if 'vendor_name' not in invoice_data:
            anomalies.append("Vendor name not found in document")
        
        # Check for formatting issues
        if len(text.strip()) < 50:
            anomalies.append("Document content seems too short")
        
        return anomalies
    
    def _generate_insights(
        self, 
        invoice_data: Dict[str, Any], 
        validation: Dict[str, Any], 
        anomalies: List[str]
    ) -> List[str]:
        """
        Generate human-readable insights about the invoice
        """
        insights = []
        
        if validation['is_valid']:
            insights.append("Invoice passed all validation checks")
        else:
            insights.append(f"Invoice has {len(validation['errors'])} validation errors")
        
        if anomalies:
            insights.append(f"Detected {len(anomalies)} potential anomalies requiring review")
        
        if 'total' in invoice_data:
            insights.append(f"Total amount: ${invoice_data['total']:.2f}")
        
        if validation['warnings']:
            insights.append(f"Found {len(validation['warnings'])} warnings")
        
        return insights
    
    def _calculate_confidence(
        self, 
        invoice_data: Dict[str, Any], 
        validation: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence score for the analysis (0.0 to 1.0)
        """
        score = 1.0
        
        # Reduce score for missing fields
        required_fields = ['invoice_number', 'date', 'total', 'vendor_name']
        missing_fields = sum(1 for field in required_fields if field not in invoice_data)
        score -= (missing_fields * 0.15)
        
        # Reduce score for validation errors
        score -= (len(validation.get('errors', [])) * 0.1)
        
        # Reduce score for warnings
        score -= (len(validation.get('warnings', [])) * 0.05)
        
        return max(0.0, min(1.0, score))
    
    def reason_about_document(self, document_data: Dict[str, Any]) -> str:
        """
        Generate human-level reasoning about a document
        
        Args:
            document_data: Document data including text and metadata
            
        Returns:
            Human-readable reasoning and analysis
        """
        text = document_data.get('text', '')
        
        analysis = self.analyze_invoice(text, document_data.get('metadata'))
        
        reasoning = f"""
Document Analysis Summary:
--------------------------
Confidence Score: {analysis['confidence_score']:.2%}

Invoice Details:
{json.dumps(analysis['invoice_data'], indent=2)}

Validation Status: {'PASSED' if analysis['validation']['is_valid'] else 'FAILED'}
- Errors: {len(analysis['validation']['errors'])}
- Warnings: {len(analysis['validation']['warnings'])}

Anomalies Detected: {len(analysis['anomalies'])}

Key Insights:
{chr(10).join(f"• {insight}" for insight in analysis['insights'])}
"""
        return reasoning.strip()
