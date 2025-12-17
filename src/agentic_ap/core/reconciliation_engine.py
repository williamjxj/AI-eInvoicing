"""
Reconciliation Engine - Third capability: RECONCILE
Matches, validates, and reconciles financial data across documents
Uses AI-powered matching algorithms for intelligent reconciliation
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import difflib

logger = logging.getLogger(__name__)


class ReconciliationEngine:
    """
    Reconciles financial data across multiple documents and sources
    Uses AI-powered matching to handle variations in data formats
    Designed for cost-effective reconciliation at scale
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize reconciliation engine with configuration
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.tolerance = self.config.get('amount_tolerance', 0.01)
        logger.info("ReconciliationEngine initialized")
    
    def reconcile_invoice(
        self, 
        invoice_data: Dict[str, Any], 
        reference_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Reconcile invoice data against reference data (PO, ERP system, etc.)
        
        Args:
            invoice_data: Analyzed invoice data
            reference_data: Reference data from another source
            
        Returns:
            Reconciliation results with matches and discrepancies
        """
        logger.info("Reconciling invoice data")
        
        matches = []
        discrepancies = []
        
        # Reconcile amounts
        amount_result = self._reconcile_amounts(
            invoice_data.get('total'), 
            reference_data.get('total')
        )
        if amount_result['matched']:
            matches.append(amount_result)
        else:
            discrepancies.append(amount_result)
        
        # Reconcile invoice numbers
        invoice_num_result = self._reconcile_identifiers(
            invoice_data.get('invoice_number'),
            reference_data.get('invoice_number'),
            'invoice_number'
        )
        if invoice_num_result['matched']:
            matches.append(invoice_num_result)
        else:
            discrepancies.append(invoice_num_result)
        
        # Reconcile vendor information
        vendor_result = self._reconcile_text(
            invoice_data.get('vendor_name'),
            reference_data.get('vendor_name'),
            'vendor_name'
        )
        if vendor_result['matched']:
            matches.append(vendor_result)
        else:
            discrepancies.append(vendor_result)
        
        # Reconcile dates
        date_result = self._reconcile_dates(
            invoice_data.get('date'),
            reference_data.get('date')
        )
        if date_result['matched']:
            matches.append(date_result)
        else:
            discrepancies.append(date_result)
        
        # Calculate reconciliation score
        total_checks = len(matches) + len(discrepancies)
        reconciliation_score = len(matches) / total_checks if total_checks > 0 else 0.0
        
        return {
            'reconciled': len(discrepancies) == 0,
            'reconciliation_score': reconciliation_score,
            'matches': matches,
            'discrepancies': discrepancies,
            'summary': self._generate_reconciliation_summary(matches, discrepancies)
        }
    
    def _reconcile_amounts(
        self, 
        amount1: Optional[float], 
        amount2: Optional[float]
    ) -> Dict[str, Any]:
        """
        Reconcile monetary amounts with tolerance
        """
        if amount1 is None or amount2 is None:
            return {
                'field': 'total',
                'matched': False,
                'reason': 'Missing amount data',
                'value1': amount1,
                'value2': amount2
            }
        
        difference = abs(amount1 - amount2)
        matched = difference <= self.tolerance
        
        return {
            'field': 'total',
            'matched': matched,
            'value1': amount1,
            'value2': amount2,
            'difference': difference,
            'tolerance': self.tolerance,
            'reason': 'Amounts match within tolerance' if matched else f'Difference of ${difference:.2f} exceeds tolerance'
        }
    
    def _reconcile_identifiers(
        self, 
        id1: Optional[str], 
        id2: Optional[str],
        field_name: str
    ) -> Dict[str, Any]:
        """
        Reconcile identifier fields (invoice numbers, PO numbers, etc.)
        """
        if id1 is None or id2 is None:
            return {
                'field': field_name,
                'matched': False,
                'reason': f'Missing {field_name}',
                'value1': id1,
                'value2': id2
            }
        
        # Normalize identifiers (remove spaces, hyphens, case)
        normalized1 = str(id1).replace(' ', '').replace('-', '').upper()
        normalized2 = str(id2).replace(' ', '').replace('-', '').upper()
        
        matched = normalized1 == normalized2
        
        return {
            'field': field_name,
            'matched': matched,
            'value1': id1,
            'value2': id2,
            'reason': f'{field_name} matches' if matched else f'{field_name} mismatch'
        }
    
    def _reconcile_text(
        self, 
        text1: Optional[str], 
        text2: Optional[str],
        field_name: str,
        similarity_threshold: float = 0.8
    ) -> Dict[str, Any]:
        """
        Reconcile text fields using fuzzy matching
        Handles variations in vendor names, descriptions, etc.
        """
        if text1 is None or text2 is None:
            return {
                'field': field_name,
                'matched': False,
                'reason': f'Missing {field_name}',
                'value1': text1,
                'value2': text2
            }
        
        # Calculate similarity using difflib
        similarity = difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        matched = similarity >= similarity_threshold
        
        return {
            'field': field_name,
            'matched': matched,
            'value1': text1,
            'value2': text2,
            'similarity': similarity,
            'threshold': similarity_threshold,
            'reason': f'{field_name} matches (similarity: {similarity:.2%})' if matched 
                     else f'{field_name} similarity too low ({similarity:.2%})'
        }
    
    def _reconcile_dates(
        self, 
        date1: Optional[str], 
        date2: Optional[str],
        tolerance_days: int = 0
    ) -> Dict[str, Any]:
        """
        Reconcile date fields with optional tolerance
        """
        if date1 is None or date2 is None:
            return {
                'field': 'date',
                'matched': False,
                'reason': 'Missing date',
                'value1': date1,
                'value2': date2
            }
        
        # For simplicity, do string comparison
        # In production, would parse dates and compare with tolerance
        matched = date1 == date2
        
        return {
            'field': 'date',
            'matched': matched,
            'value1': date1,
            'value2': date2,
            'reason': 'Dates match' if matched else 'Date mismatch'
        }
    
    def reconcile_batch(
        self, 
        invoices: List[Dict[str, Any]], 
        reference_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Reconcile multiple invoices against reference data in batch
        
        Args:
            invoices: List of invoice data dictionaries
            reference_data: List of reference data dictionaries
            
        Returns:
            Batch reconciliation results
        """
        logger.info(f"Reconciling batch of {len(invoices)} invoices")
        
        results = []
        unmatched_invoices = []
        unmatched_references = []
        
        # Create a copy of reference data to track matched items
        remaining_references = reference_data.copy()
        
        for invoice in invoices:
            # Try to find matching reference
            best_match = None
            best_score = 0.0
            
            for ref in remaining_references:
                # Simple matching by invoice number
                if (invoice.get('invoice_number') and 
                    ref.get('invoice_number') and
                    invoice['invoice_number'] == ref['invoice_number']):
                    
                    reconciliation = self.reconcile_invoice(invoice, ref)
                    score = reconciliation['reconciliation_score']
                    
                    if score > best_score:
                        best_match = ref
                        best_score = score
            
            if best_match:
                reconciliation = self.reconcile_invoice(invoice, best_match)
                results.append({
                    'invoice': invoice,
                    'reference': best_match,
                    'reconciliation': reconciliation
                })
                remaining_references.remove(best_match)
            else:
                unmatched_invoices.append(invoice)
        
        unmatched_references = remaining_references
        
        return {
            'total_invoices': len(invoices),
            'total_references': len(reference_data),
            'matched': len(results),
            'unmatched_invoices': len(unmatched_invoices),
            'unmatched_references': len(unmatched_references),
            'results': results,
            'unmatched_invoice_list': unmatched_invoices,
            'unmatched_reference_list': unmatched_references
        }
    
    def _generate_reconciliation_summary(
        self, 
        matches: List[Dict], 
        discrepancies: List[Dict]
    ) -> str:
        """
        Generate human-readable reconciliation summary
        """
        total = len(matches) + len(discrepancies)
        
        summary = f"Reconciliation Summary:\n"
        summary += f"- Total fields checked: {total}\n"
        summary += f"- Matched: {len(matches)}\n"
        summary += f"- Discrepancies: {len(discrepancies)}\n"
        
        if discrepancies:
            summary += "\nDiscrepancies found in:\n"
            for disc in discrepancies:
                summary += f"  • {disc['field']}: {disc['reason']}\n"
        else:
            summary += "\nAll fields reconciled successfully!"
        
        return summary
    
    def generate_reconciliation_report(
        self, 
        reconciliation_result: Dict[str, Any]
    ) -> str:
        """
        Generate detailed reconciliation report
        
        Args:
            reconciliation_result: Result from reconcile_invoice or reconcile_batch
            
        Returns:
            Formatted report string
        """
        report = "=" * 60 + "\n"
        report += "RECONCILIATION REPORT\n"
        report += "=" * 60 + "\n\n"
        
        if 'total_invoices' in reconciliation_result:
            # Batch report
            report += f"Batch Reconciliation Results:\n"
            report += f"  Total Invoices: {reconciliation_result['total_invoices']}\n"
            report += f"  Total References: {reconciliation_result['total_references']}\n"
            report += f"  Successfully Matched: {reconciliation_result['matched']}\n"
            report += f"  Unmatched Invoices: {reconciliation_result['unmatched_invoices']}\n"
            report += f"  Unmatched References: {reconciliation_result['unmatched_references']}\n\n"
        else:
            # Single invoice report
            report += f"Reconciliation Status: {'RECONCILED' if reconciliation_result['reconciled'] else 'DISCREPANCIES FOUND'}\n"
            report += f"Reconciliation Score: {reconciliation_result['reconciliation_score']:.2%}\n\n"
            report += reconciliation_result['summary']
        
        report += "\n" + "=" * 60 + "\n"
        
        return report
