# AgenticAP Architecture

## Overview

AgenticAP is built on a modular architecture that enables three core AI capabilities: READ, REASON, and RECONCILE. The platform leverages open-source technologies to provide cost-effective financial document processing with human-level reasoning.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AgenticAP Platform                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Agentic Engine                          │  │
│  │              (Orchestration & Coordination)                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐     ┌──────────────┐     │
│  │  Document   │      │  Reasoning  │     │Reconciliation│     │
│  │   Reader    │      │   Engine    │     │   Engine     │     │
│  │   (READ)    │      │  (REASON)   │     │  (RECONCILE) │     │
│  └─────────────┘      └─────────────┘     └──────────────┘     │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐     ┌──────────────┐     │
│  │ • PDF Parse │      │ • LLM Model │     │ • Fuzzy Match│     │
│  │ • OCR       │      │ • Pattern   │     │ • Amount     │     │
│  │ • Multi-fmt │      │   Recognition│     │   Validation │     │
│  │ • Metadata  │      │ • Validation│     │ • Date Match │     │
│  └─────────────┘      │ • Anomaly   │     │ • Batch Proc │     │
│                       │   Detection │     └──────────────┘     │
│                       └─────────────┘                           │
│                                                                   │
├─────────────────────────────────────────────────────────────────┤
│                         API Layer (FastAPI)                      │
├─────────────────────────────────────────────────────────────────┤
│                   Configuration & Utilities                      │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Agentic Engine (`agentic_engine.py`)

The central orchestrator that coordinates all three capabilities:

**Responsibilities:**
- Initialize and manage all sub-engines
- Coordinate the READ → REASON → RECONCILE pipeline
- Calculate overall confidence scores
- Generate comprehensive reports
- Handle batch processing

**Key Methods:**
- `process_invoice()`: End-to-end single invoice processing
- `process_batch()`: Batch processing for multiple invoices
- `generate_report()`: Human-readable report generation
- `get_capabilities()`: Platform capability inspection

### 2. Document Reader (`document_reader.py`)

Handles document ingestion and content extraction:

**Capabilities:**
- PDF text extraction using PyPDF2
- Image OCR using Pytesseract/EasyOCR
- Metadata extraction
- Multi-format support

**Supported Formats:**
- PDF documents
- Images (PNG, JPG, JPEG, TIFF)
- Future: DOCX, XLSX, XML

**Key Features:**
- Graceful degradation when dependencies missing
- Error handling and logging
- Batch reading support

### 3. Reasoning Engine (`reasoning_engine.py`)

Provides AI-powered analysis and understanding:

**Capabilities:**
- Field extraction using pattern recognition
- Business logic validation
- Anomaly detection
- Confidence scoring
- Insight generation

**Analysis Process:**
1. Extract invoice fields (number, date, amounts, vendor)
2. Validate business logic (calculations, required fields)
3. Detect anomalies (unusual amounts, missing data)
4. Generate insights and confidence scores

**AI Integration:**
- Designed for LLM integration (Mistral, Llama, etc.)
- Pattern-based extraction as fallback
- Extensible for custom reasoning logic

### 4. Reconciliation Engine (`reconciliation_engine.py`)

Matches and validates data across sources:

**Capabilities:**
- Amount reconciliation with tolerance
- Fuzzy text matching for vendor names
- Date matching and validation
- Batch reconciliation
- Discrepancy reporting

**Matching Strategies:**
- **Amounts**: Tolerance-based (default: $0.01)
- **Text**: Fuzzy matching using difflib (80% threshold)
- **Identifiers**: Normalized exact matching
- **Dates**: Format-aware comparison

### 5. API Layer (`api/main.py`)

RESTful API built with FastAPI:

**Endpoints:**
- `GET /`: API information and capabilities
- `GET /capabilities`: Platform capabilities
- `GET /health`: Health check
- `POST /process`: Single invoice processing
- `POST /process_with_reference`: Processing with structured reference

**Features:**
- Async file handling
- Automatic documentation (Swagger/ReDoc)
- Error handling and logging
- Response models with Pydantic

## Data Flow

### Single Invoice Processing

```
1. Upload Document
   ↓
2. Document Reader (READ)
   • Extract text/content
   • Parse metadata
   ↓
3. Reasoning Engine (REASON)
   • Extract fields
   • Validate data
   • Detect anomalies
   • Calculate confidence
   ↓
4. Reconciliation Engine (RECONCILE)
   • Match with reference
   • Identify discrepancies
   • Calculate reconciliation score
   ↓
5. Generate Report
   • Compile results
   • Create insights
   • Return response
```

### Batch Processing

```
1. Upload Multiple Documents
   ↓
2. For Each Document:
   • Process through pipeline
   • Collect results
   ↓
3. Aggregate Results
   • Count successes/failures
   • Generate batch statistics
   ↓
4. Return Batch Report
```

## Technology Stack

### Core Python Libraries

**AI/ML:**
- `transformers`: LLM integration
- `torch`: Deep learning backend
- `langchain`: LLM orchestration

**Document Processing:**
- `PyPDF2`: PDF parsing
- `Pillow`: Image handling
- `pytesseract`: OCR engine
- `easyocr`: Advanced OCR
- `python-docx`: Word documents
- `openpyxl`: Excel files

**Data Processing:**
- `pandas`: Data manipulation
- `numpy`: Numerical operations

**API:**
- `fastapi`: Modern web framework
- `uvicorn`: ASGI server
- `pydantic`: Data validation

**Utilities:**
- `pyyaml`: Configuration
- `python-dotenv`: Environment variables

## Configuration

### config.yaml Structure

```yaml
app:
  name: AgenticAP
  version: 1.0.0

agentic_ai:
  model:
    name: mistral-7b      # Open-source LLM
    provider: local       # Run locally
    temperature: 0.1      # Precision for finance
    
  capabilities:
    read: true
    reason: true
    reconcile: true

document_processing:
  supported_formats: [pdf, png, jpg, ...]
  ocr:
    engine: tesseract
    confidence_threshold: 0.7

financial_rules:
  invoice_fields: [...]
  validation:
    amount_tolerance: 0.01
    currency: USD

api:
  host: 0.0.0.0
  port: 8000
```

## Extensibility

### Adding New Document Formats

1. Update `DocumentReader._read_<format>()` method
2. Add format to `supported_formats` in config
3. Add parser dependencies to requirements.txt

### Custom Reasoning Logic

1. Extend `ReasoningEngine` class
2. Override `analyze_invoice()` or add new methods
3. Update configuration for custom rules

### Integration with External Systems

1. Create new agent in `agents/` directory
2. Implement data fetching/posting
3. Integrate with reconciliation engine

### LLM Integration

The platform is designed for easy LLM integration:

```python
# Example: Integrate with LangChain
from langchain import OpenAI, PromptTemplate

class EnhancedReasoningEngine(ReasoningEngine):
    def __init__(self, config):
        super().__init__(config)
        self.llm = OpenAI(model_name="gpt-3.5-turbo")
    
    def analyze_invoice(self, text, metadata):
        # Use LLM for deeper analysis
        prompt = f"Analyze this invoice: {text}"
        analysis = self.llm(prompt)
        return analysis
```

## Performance Considerations

### Scalability
- Batch processing for high volume
- Async API for concurrent requests
- Local LLM for low latency

### Cost Optimization
- Open-source models (no API fees)
- Local processing (no cloud costs)
- Efficient caching and reuse

### Accuracy
- Multiple validation layers
- Confidence scoring
- Human-in-the-loop for low confidence

## Security

- Input validation on all endpoints
- File type verification
- Temporary file cleanup
- No credential storage in code
- Environment variable configuration

## Future Enhancements

1. **Enhanced LLM Integration**: Full integration with open-source LLMs
2. **Learning System**: Improve accuracy over time
3. **Multi-language Support**: Process invoices in multiple languages
4. **Advanced OCR**: Deep learning-based OCR for complex layouts
5. **Workflow Automation**: Integration with ERP systems
6. **Mobile App**: Mobile document capture and processing
7. **Blockchain**: Immutable audit trail for reconciliations
8. **Analytics Dashboard**: Visualization and reporting

## Conclusion

AgenticAP's architecture is designed for:
- **Modularity**: Easy to extend and customize
- **Cost-effectiveness**: Leverages open-source stack
- **Scalability**: Handles growing volumes
- **Intelligence**: Human-level reasoning with AI
- **Integration**: API-first design for easy adoption
