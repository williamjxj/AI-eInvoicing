"""
Agentic Engine - Main orchestrator for READ, REASON, and RECONCILE capabilities
Provides human-level AI reasoning for financial document processing
Built on cost-effective open-source stack
"""

import logging
from typing import Dict, List, Any, Optional
import yaml
from pathlib import Path

from .document_reader import DocumentReader
from .reasoning_engine import ReasoningEngine
from .reconciliation_engine import ReconciliationEngine

logger = logging.getLogger(__name__)


class AgenticEngine:
    """
    Main Agentic AI engine that orchestrates the three core capabilities:
    1. READ - Document reading and extraction
    2. REASON - AI-powered analysis and understanding
    3. RECONCILE - Data matching and validation
    
    Built on open-source stack to undercut expensive legacy systems
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Agentic Engine with all three capabilities
        
        Args:
            config_path: Optional path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize the three core engines
        self.document_reader = DocumentReader(self.config.get('document_processing'))
        self.reasoning_engine = ReasoningEngine(self.config.get('agentic_ai'))
        self.reconciliation_engine = ReconciliationEngine(self.config.get('financial_rules'))
        
        logger.info("AgenticEngine initialized with READ, REASON, and RECONCILE capabilities")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def process_invoice(
        self, 
        file_path: str, 
        reference_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Complete end-to-end invoice processing with READ, REASON, and RECONCILE
        
        Args:
            file_path: Path to invoice document
            reference_data: Optional reference data for reconciliation
            
        Returns:
            Complete processing results including all three capabilities
        """
        logger.info(f"Processing invoice: {file_path}")
        
        # Step 1: READ - Extract content from document
        logger.info("Step 1/3: READ - Extracting document content")
        document_data = self.document_reader.read_document(file_path)
        
        if 'error' in document_data:
            return {
                'success': False,
                'error': document_data['error'],
                'file_path': file_path
            }
        
        # Step 2: REASON - Analyze and understand the invoice
        logger.info("Step 2/3: REASON - Analyzing invoice with AI")
        analysis = self.reasoning_engine.analyze_invoice(
            document_data['text'],
            document_data.get('metadata')
        )
        
        # Step 3: RECONCILE - Match against reference data if provided
        reconciliation = None
        if reference_data:
            logger.info("Step 3/3: RECONCILE - Matching against reference data")
            reconciliation = self.reconciliation_engine.reconcile_invoice(
                analysis['invoice_data'],
                reference_data
            )
        
        # Compile complete results
        result = {
            'success': True,
            'file_path': file_path,
            'document': {
                'format': document_data['format'],
                'file_name': document_data.get('file_name'),
                'pages': document_data.get('pages'),
                'metadata': document_data.get('metadata', {})
            },
            'analysis': analysis,
            'reconciliation': reconciliation,
            'overall_confidence': self._calculate_overall_confidence(analysis, reconciliation)
        }
        
        return result
    
    def process_batch(
        self, 
        file_paths: List[str], 
        reference_data_list: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Process multiple invoices in batch mode
        
        Args:
            file_paths: List of invoice file paths
            reference_data_list: Optional list of reference data for reconciliation
            
        Returns:
            Batch processing results
        """
        logger.info(f"Processing batch of {len(file_paths)} invoices")
        
        results = []
        successful = 0
        failed = 0
        
        for i, file_path in enumerate(file_paths):
            reference_data = None
            if reference_data_list and i < len(reference_data_list):
                reference_data = reference_data_list[i]
            
            try:
                result = self.process_invoice(file_path, reference_data)
                results.append(result)
                
                if result['success']:
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {str(e)}")
                results.append({
                    'success': False,
                    'file_path': file_path,
                    'error': str(e)
                })
                failed += 1
        
        return {
            'total': len(file_paths),
            'successful': successful,
            'failed': failed,
            'results': results
        }
    
    def _calculate_overall_confidence(
        self, 
        analysis: Dict[str, Any], 
        reconciliation: Optional[Dict[str, Any]]
    ) -> float:
        """
        Calculate overall confidence score for the processing
        """
        confidence = analysis.get('confidence_score', 0.0)
        
        # Boost confidence if reconciliation passed
        if reconciliation and reconciliation.get('reconciled'):
            confidence = min(1.0, confidence * 1.1)
        
        # Reduce confidence if reconciliation failed
        if reconciliation and not reconciliation.get('reconciled'):
            reconciliation_score = reconciliation.get('reconciliation_score', 0.0)
            confidence = (confidence + reconciliation_score) / 2
        
        return confidence
    
    def generate_report(self, processing_result: Dict[str, Any]) -> str:
        """
        Generate comprehensive human-readable report
        
        Args:
            processing_result: Result from process_invoice or process_batch
            
        Returns:
            Formatted report string
        """
        if not processing_result.get('success'):
            return f"Processing failed: {processing_result.get('error', 'Unknown error')}"
        
        report = "=" * 70 + "\n"
        report += "AGENTIC AI INVOICE PROCESSING REPORT\n"
        report += "=" * 70 + "\n\n"
        
        # Document information
        report += "DOCUMENT INFORMATION:\n"
        report += "-" * 70 + "\n"
        report += f"File: {processing_result.get('file_path')}\n"
        doc = processing_result.get('document', {})
        report += f"Format: {doc.get('format', 'Unknown')}\n"
        if doc.get('pages'):
            report += f"Pages: {doc['pages']}\n"
        report += f"\n"
        
        # Analysis results
        analysis = processing_result.get('analysis', {})
        report += "AI ANALYSIS RESULTS (REASON):\n"
        report += "-" * 70 + "\n"
        report += f"Confidence Score: {analysis.get('confidence_score', 0):.2%}\n"
        report += f"Validation Status: {'PASSED' if analysis.get('validation', {}).get('is_valid') else 'FAILED'}\n"
        
        invoice_data = analysis.get('invoice_data', {})
        if invoice_data:
            report += f"\nExtracted Invoice Data:\n"
            for key, value in invoice_data.items():
                report += f"  {key}: {value}\n"
        
        insights = analysis.get('insights', [])
        if insights:
            report += f"\nKey Insights:\n"
            for insight in insights:
                report += f"  • {insight}\n"
        
        anomalies = analysis.get('anomalies', [])
        if anomalies:
            report += f"\nAnomalies Detected:\n"
            for anomaly in anomalies:
                report += f"  ⚠ {anomaly}\n"
        
        # Reconciliation results
        if processing_result.get('reconciliation'):
            reconciliation = processing_result['reconciliation']
            report += f"\nRECONCILIATION RESULTS:\n"
            report += "-" * 70 + "\n"
            report += f"Status: {'RECONCILED ✓' if reconciliation.get('reconciled') else 'DISCREPANCIES FOUND ✗'}\n"
            report += f"Score: {reconciliation.get('reconciliation_score', 0):.2%}\n"
            report += f"Matches: {len(reconciliation.get('matches', []))}\n"
            report += f"Discrepancies: {len(reconciliation.get('discrepancies', []))}\n"
            
            if reconciliation.get('discrepancies'):
                report += f"\nDiscrepancy Details:\n"
                for disc in reconciliation['discrepancies']:
                    report += f"  • {disc['field']}: {disc['reason']}\n"
        
        # Overall confidence
        report += f"\nOVERALL CONFIDENCE: {processing_result.get('overall_confidence', 0):.2%}\n"
        
        report += "\n" + "=" * 70 + "\n"
        
        return report
    
    def get_capabilities(self) -> Dict[str, bool]:
        """
        Return information about enabled capabilities
        
        Returns:
            Dictionary of capabilities and their status
        """
        return {
            'read': True,
            'reason': True,
            'reconcile': True,
            'cost_effective': True,
            'open_source': True,
            'human_level_reasoning': True
        }
