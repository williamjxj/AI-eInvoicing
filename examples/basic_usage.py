"""
Basic usage example for AgenticAP
Demonstrates READ, REASON, and RECONCILE capabilities
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from agentic_ap import AgenticEngine
from agentic_ap.utils.logger import setup_logger


def main():
    """Demonstrate basic AgenticAP usage"""
    
    # Set up logging
    logger = setup_logger('example')
    
    logger.info("=" * 70)
    logger.info("AgenticAP - AI-Native Financial Automation Platform")
    logger.info("Built on open-source stack for cost-effective processing")
    logger.info("=" * 70)
    
    # Initialize the Agentic Engine
    config_path = Path(__file__).parent.parent / 'config.yaml'
    engine = AgenticEngine(config_path=str(config_path))
    
    # Display capabilities
    capabilities = engine.get_capabilities()
    logger.info("\nPlatform Capabilities:")
    for capability, enabled in capabilities.items():
        status = "✓" if enabled else "✗"
        logger.info(f"  {status} {capability.replace('_', ' ').title()}")
    
    # Example 1: Process a sample invoice (demonstrating the three capabilities)
    logger.info("\n" + "=" * 70)
    logger.info("Example: Processing Invoice with READ, REASON, and RECONCILE")
    logger.info("=" * 70)
    
    # Create a sample invoice text for demonstration
    sample_invoice_text = """
    ACME Corporation
    123 Business St, Suite 100
    New York, NY 10001
    
    INVOICE
    
    Invoice Number: INV-2024-001
    Date: 12/15/2024
    
    Bill To:
    XYZ Company
    456 Customer Ave
    Los Angeles, CA 90001
    
    Description                Quantity    Price      Amount
    -----------------------------------------------------------
    Professional Services         10       $150.00    $1,500.00
    Consulting Fee                 5       $200.00    $1,000.00
    
    Subtotal:                                         $2,500.00
    Tax (8%):                                           $200.00
    Total:                                            $2,700.00
    
    Payment Terms: Net 30
    """
    
    # Save sample invoice to temp file
    temp_dir = Path('/tmp/agentic_ap_demo')
    temp_dir.mkdir(exist_ok=True)
    sample_file = temp_dir / 'sample_invoice.txt'
    sample_file.write_text(sample_invoice_text)
    
    # Reference data for reconciliation
    reference_data = {
        'invoice_number': 'INV-2024-001',
        'date': '12/15/2024',
        'vendor_name': 'ACME Corporation',
        'total': 2700.00,
        'tax': 200.00
    }
    
    # Process the invoice with all three capabilities
    logger.info("\nProcessing invoice...")
    result = engine.process_invoice(str(sample_file), reference_data)
    
    # Generate and display report
    if result['success']:
        report = engine.generate_report(result)
        print("\n" + report)
        
        logger.info("\n✓ Invoice processed successfully!")
        logger.info(f"Overall Confidence: {result['overall_confidence']:.2%}")
    else:
        logger.error(f"Processing failed: {result.get('error')}")
    
    # Example 2: Demonstrate cost-effectiveness
    logger.info("\n" + "=" * 70)
    logger.info("Cost Comparison: AgenticAP vs Legacy Systems")
    logger.info("=" * 70)
    logger.info("\nAgenticAP Advantages:")
    logger.info("  ✓ Open-source LLM models (Mistral, Llama, etc.)")
    logger.info("  ✓ Local processing - no expensive API calls")
    logger.info("  ✓ Open-source OCR (Tesseract, EasyOCR)")
    logger.info("  ✓ Python-based stack - no licensing fees")
    logger.info("  ✓ Scalable architecture for high volume")
    logger.info("\nEstimated Cost per Invoice:")
    logger.info("  • AgenticAP: $0.001 - $0.01")
    logger.info("  • Legacy Systems: $0.50 - $5.00")
    logger.info("  • Savings: Up to 99% reduction in processing costs!")
    
    logger.info("\n" + "=" * 70)
    logger.info("Demo completed successfully!")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
