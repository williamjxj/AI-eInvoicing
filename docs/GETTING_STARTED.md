# Getting Started with AgenticAP

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Optional: Tesseract OCR for image processing

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/williamjxj/AgenticAP.git
cd AgenticAP
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR (Optional, for image processing)

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

## Quick Start Guide

### Running the Basic Example

```bash
python examples/basic_usage.py
```

This will:
1. Initialize the AgenticAP engine
2. Process a sample invoice
3. Demonstrate READ, REASON, and RECONCILE capabilities
4. Show cost comparison with legacy systems

### Processing Your First Invoice

```python
from agentic_ap import AgenticEngine

# Initialize the engine
engine = AgenticEngine(config_path='config.yaml')

# Process an invoice
result = engine.process_invoice('path/to/invoice.pdf')

# Display results
print(engine.generate_report(result))
```

### With Reconciliation

```python
# Define reference data
reference_data = {
    'invoice_number': 'INV-001',
    'date': '2024-01-15',
    'vendor_name': 'ACME Corp',
    'total': 1000.00,
    'tax': 80.00
}

# Process with reconciliation
result = engine.process_invoice('invoice.pdf', reference_data)

# Check reconciliation status
if result['reconciliation']['reconciled']:
    print("✓ Invoice reconciled successfully!")
else:
    print("✗ Discrepancies found")
    print(result['reconciliation']['summary'])
```

## Using the API

### Start the API Server

```bash
cd src
python -m agentic_ap.api.main
```

Or with uvicorn:
```bash
uvicorn agentic_ap.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Access API Documentation

Open your browser to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Make API Requests

**Check capabilities:**
```bash
curl http://localhost:8000/capabilities
```

**Process an invoice:**
```bash
curl -X POST "http://localhost:8000/process" \
  -F "file=@invoice.pdf"
```

**Process with reference data:**
```bash
curl -X POST "http://localhost:8000/process" \
  -F "file=@invoice.pdf" \
  -F 'reference_data={"invoice_number": "INV-001", "total": 1000.00}'
```

## Configuration

Edit `config.yaml` to customize behavior:

```yaml
agentic_ai:
  model:
    name: "mistral-7b"  # Change to your preferred LLM
    temperature: 0.1     # Adjust for more/less creative responses

document_processing:
  ocr:
    confidence_threshold: 0.7  # Adjust OCR confidence requirement

financial_rules:
  validation:
    amount_tolerance: 0.01  # Tolerance for amount matching
    currency: "USD"         # Default currency
```

## Understanding the Output

### Processing Result Structure

```python
{
    'success': True,
    'file_path': 'invoice.pdf',
    'document': {
        'format': 'pdf',
        'pages': 2,
        'metadata': {...}
    },
    'analysis': {
        'invoice_data': {
            'invoice_number': 'INV-001',
            'date': '2024-01-15',
            'total': 1000.00,
            ...
        },
        'validation': {
            'is_valid': True,
            'errors': [],
            'warnings': []
        },
        'anomalies': [],
        'insights': [...],
        'confidence_score': 0.95
    },
    'reconciliation': {
        'reconciled': True,
        'reconciliation_score': 1.0,
        'matches': [...],
        'discrepancies': []
    },
    'overall_confidence': 0.95
}
```

### Confidence Scores

- **0.9 - 1.0**: High confidence, safe to auto-process
- **0.7 - 0.9**: Good confidence, minimal review needed
- **0.5 - 0.7**: Medium confidence, human review recommended
- **< 0.5**: Low confidence, requires human review

## Batch Processing

Process multiple invoices:

```python
file_paths = [
    'invoice1.pdf',
    'invoice2.pdf',
    'invoice3.pdf'
]

results = engine.process_batch(file_paths)

print(f"Processed: {results['successful']} successful, {results['failed']} failed")
```

## Troubleshooting

### Common Issues

**1. "Module not found" errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're in the correct virtual environment

**2. OCR not working**
- Install Tesseract OCR on your system
- Verify installation: `tesseract --version`

**3. Low confidence scores**
- Check document quality (resolution, clarity)
- Verify document format is supported
- Review extracted text in the output

**4. Reconciliation failures**
- Check reference data format matches expected structure
- Verify amounts are in the same currency
- Adjust tolerance in config.yaml if needed

## Next Steps

1. **Read the Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Review Cost Analysis**: See [COST_ANALYSIS.md](COST_ANALYSIS.md)
3. **Customize Configuration**: Edit `config.yaml`
4. **Extend Functionality**: Add custom agents in `src/agentic_ap/agents/`
5. **Integrate with Your Systems**: Use the REST API

## Support

- Documentation: `/docs` directory
- Examples: `/examples` directory
- Issues: GitHub Issues

## Performance Tips

1. **Batch Processing**: Process multiple invoices together for efficiency
2. **Local LLM**: Use local models to eliminate API latency
3. **Caching**: Implement caching for frequently accessed data
4. **Parallel Processing**: Use Python's multiprocessing for large batches
5. **GPU Acceleration**: Enable GPU for faster LLM inference

---

Happy processing with AgenticAP! 🚀
