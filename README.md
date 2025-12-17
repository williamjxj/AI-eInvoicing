# AgenticAP

An AI-native financial automation platform dedicated to processing heterogeneous invoice formats with human-level reasoning.

## 🎯 Core Capabilities: READ, REASON, and RECONCILE

AgenticAP is built on **Agentic AI** technology that provides three fundamental capabilities for financial document processing:

### 1. 📖 READ
- **Intelligent Document Extraction**: Processes multiple formats (PDF, PNG, JPG, TIFF, DOCX, XLSX)
- **Advanced OCR**: Uses open-source OCR engines (Tesseract, EasyOCR) for image-based documents
- **Multi-format Support**: Handles heterogeneous invoice formats automatically
- **Metadata Extraction**: Captures document properties and structure

### 2. 🧠 REASON
- **Human-Level AI Reasoning**: Understands invoice content with contextual awareness
- **Pattern Recognition**: Identifies key fields (invoice numbers, dates, amounts, vendors)
- **Business Logic Validation**: Applies financial rules and calculations
- **Anomaly Detection**: Flags suspicious patterns or inconsistencies
- **Confidence Scoring**: Provides reliability metrics for each analysis

### 3. 🔄 RECONCILE
- **Intelligent Matching**: Fuzzy matching for vendor names and text fields
- **Amount Reconciliation**: Handles rounding and tolerance-based matching
- **Batch Processing**: Reconciles multiple invoices against reference data
- **Discrepancy Reporting**: Detailed reports on matches and mismatches
- **Multi-source Validation**: Cross-references with POs, ERP systems, databases

## 💰 Cost-Effective Open-Source Stack

AgenticAP is designed to **undercut expensive legacy incumbents** by leveraging a completely open-source technology stack:

### Technology Stack
- **AI/ML**: Transformers, PyTorch, LangChain (open-source LLMs)
- **Document Processing**: PyPDF2, Pillow, python-docx
- **OCR**: Pytesseract, EasyOCR
- **Data Processing**: Pandas, NumPy, OpenPyXL
- **API Framework**: FastAPI, Uvicorn
- **Language**: Python 3.8+

### Cost Comparison
| Solution | Cost per Invoice | Annual Cost (10K invoices) |
|----------|-----------------|---------------------------|
| Legacy Systems | $0.50 - $5.00 | $5,000 - $50,000 |
| **AgenticAP** | **$0.001 - $0.01** | **$10 - $100** |
| **Savings** | **Up to 99%** | **Up to $49,900** |

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/williamjxj/AgenticAP.git
cd AgenticAP

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from agentic_ap import AgenticEngine

# Initialize the engine
engine = AgenticEngine(config_path='config.yaml')

# Process an invoice with all three capabilities
result = engine.process_invoice(
    file_path='invoice.pdf',
    reference_data={
        'invoice_number': 'INV-001',
        'total': 2700.00
    }
)

# Generate human-readable report
report = engine.generate_report(result)
print(report)
```

### Run Example

```bash
python examples/basic_usage.py
```

### Start API Server

```bash
# Start FastAPI server
cd src
python -m agentic_ap.api.main

# Or use uvicorn directly
uvicorn agentic_ap.api.main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

#### POST /process
Process a single invoice document

```bash
curl -X POST "http://localhost:8000/process" \
  -F "file=@invoice.pdf" \
  -F 'reference_data={"invoice_number": "INV-001", "total": 2700.00}'
```

#### GET /capabilities
Get platform capabilities

```bash
curl http://localhost:8000/capabilities
```

## 🏗️ Architecture

```
AgenticAP
├── Document Reader (READ)
│   ├── PDF Parser
│   ├── Image OCR
│   └── Multi-format Support
│
├── Reasoning Engine (REASON)
│   ├── Field Extraction
│   ├── Pattern Recognition
│   ├── Business Logic Validation
│   ├── Anomaly Detection
│   └── Confidence Scoring
│
└── Reconciliation Engine (RECONCILE)
    ├── Fuzzy Matching
    ├── Amount Validation
    ├── Date Reconciliation
    └── Batch Processing
```

## 🎯 Key Features

✅ **Human-Level Reasoning**: AI-powered understanding of financial documents  
✅ **Cost-Effective**: Up to 99% cost reduction vs legacy systems  
✅ **Open-Source Stack**: No vendor lock-in, full control  
✅ **Heterogeneous Format Support**: Handles any invoice format  
✅ **Batch Processing**: Scale to thousands of invoices  
✅ **RESTful API**: Easy integration with existing systems  
✅ **Confidence Scoring**: Know the reliability of each result  
✅ **Anomaly Detection**: Automatic fraud and error detection  

## 📊 Use Cases

- **Accounts Payable Automation**: Automate invoice processing end-to-end
- **Financial Reconciliation**: Match invoices with POs and receipts
- **Audit and Compliance**: Detect anomalies and validate data
- **Multi-vendor Management**: Handle diverse invoice formats
- **Cost Reduction**: Replace expensive legacy AP systems

## 🔧 Configuration

Edit `config.yaml` to customize:

```yaml
agentic_ai:
  model:
    name: "mistral-7b"  # Or any open-source LLM
    provider: "local"
    temperature: 0.1
  
  capabilities:
    read: true
    reason: true
    reconcile: true

document_processing:
  supported_formats:
    - "pdf"
    - "png"
    - "jpg"
    - "jpeg"
    - "tiff"
    - "docx"
    - "xlsx"

financial_rules:
  validation:
    amount_tolerance: 0.01
    date_format: "%Y-%m-%d"
    currency: "USD"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built with open-source technologies:
- Transformers (Hugging Face)
- PyTorch
- LangChain
- FastAPI
- And many more amazing open-source projects

---

**AgenticAP** - Intelligent financial automation powered by Agentic AI, designed to undercut expensive legacy systems with cost-effective open-source technology. 
