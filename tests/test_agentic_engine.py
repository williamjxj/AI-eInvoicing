"""
Tests for Agentic Engine
Validates the core READ, REASON, and RECONCILE capabilities
"""

import sys
from pathlib import Path
import tempfile

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from agentic_ap import AgenticEngine


def test_engine_initialization():
    """Test that engine initializes correctly"""
    engine = AgenticEngine()
    
    assert engine is not None
    assert engine.document_reader is not None
    assert engine.reasoning_engine is not None
    assert engine.reconciliation_engine is not None


def test_capabilities():
    """Test that all three capabilities are enabled"""
    engine = AgenticEngine()
    capabilities = engine.get_capabilities()
    
    assert capabilities['read'] is True
    assert capabilities['reason'] is True
    assert capabilities['reconcile'] is True
    assert capabilities['cost_effective'] is True
    assert capabilities['open_source'] is True


def test_process_sample_invoice():
    """Test processing a sample invoice text"""
    engine = AgenticEngine()
    
    # Create a sample invoice
    sample_text = """
    ACME Corp
    Invoice #: INV-001
    Date: 2024-01-15
    Total: $1,000.00
    Tax: $80.00
    """
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_text)
        temp_path = f.name
    
    try:
        # Process the invoice
        result = engine.process_invoice(temp_path)
        
        # Verify results
        assert result['success'] is True
        assert 'analysis' in result
        assert 'overall_confidence' in result
        assert result['overall_confidence'] > 0.0
        
        # Verify analysis contains expected data
        analysis = result['analysis']
        assert 'invoice_data' in analysis
        assert 'validation' in analysis
        assert 'confidence_score' in analysis
    finally:
        # Cleanup
        Path(temp_path).unlink()


def test_reconciliation():
    """Test invoice reconciliation capability"""
    engine = AgenticEngine()
    
    sample_text = """
    Invoice Number: INV-123
    Total: $500.00
    """
    
    reference_data = {
        'invoice_number': 'INV-123',
        'total': 500.00
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_text)
        temp_path = f.name
    
    try:
        result = engine.process_invoice(temp_path, reference_data)
        
        assert result['success'] is True
        assert 'reconciliation' in result
        assert result['reconciliation'] is not None
        
        # Should have matches since data matches
        reconciliation = result['reconciliation']
        assert 'matches' in reconciliation
        assert len(reconciliation['matches']) > 0
    finally:
        Path(temp_path).unlink()


def test_report_generation():
    """Test that reports can be generated"""
    engine = AgenticEngine()
    
    sample_text = "Invoice #: TEST-001\nTotal: $100.00"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_text)
        temp_path = f.name
    
    try:
        result = engine.process_invoice(temp_path)
        report = engine.generate_report(result)
        
        assert isinstance(report, str)
        assert len(report) > 0
        assert 'AGENTIC AI' in report
        assert 'REPORT' in report
    finally:
        Path(temp_path).unlink()


if __name__ == '__main__':
    print("Running AgenticAP tests...")
    
    test_engine_initialization()
    print("✓ Engine initialization test passed")
    
    test_capabilities()
    print("✓ Capabilities test passed")
    
    test_process_sample_invoice()
    print("✓ Sample invoice processing test passed")
    
    test_reconciliation()
    print("✓ Reconciliation test passed")
    
    test_report_generation()
    print("✓ Report generation test passed")
    
    print("\n✅ All tests passed!")
