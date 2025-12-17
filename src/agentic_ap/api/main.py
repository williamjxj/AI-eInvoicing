"""
FastAPI application for AgenticAP
Provides REST API endpoints for invoice processing
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import tempfile
import os
from pathlib import Path

from ..core.agentic_engine import AgenticEngine
from ..utils.logger import setup_logger

# Initialize logger
logger = setup_logger('api')

# Create FastAPI app
app = FastAPI(
    title="AgenticAP",
    description="AI-native financial automation platform with READ, REASON, and RECONCILE capabilities",
    version="1.0.0"
)

# Initialize Agentic Engine
config_path = Path(__file__).parent.parent.parent.parent / 'config.yaml'
engine = AgenticEngine(config_path=str(config_path) if config_path.exists() else None)


class ReferenceData(BaseModel):
    """Reference data for invoice reconciliation"""
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    vendor_name: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None


class ProcessingResponse(BaseModel):
    """Response model for invoice processing"""
    success: bool
    file_name: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = None
    reconciliation: Optional[Dict[str, Any]] = None
    overall_confidence: Optional[float] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AgenticAP",
        "version": "1.0.0",
        "description": "AI-native financial automation platform",
        "capabilities": engine.get_capabilities(),
        "endpoints": {
            "/process": "POST - Process a single invoice",
            "/capabilities": "GET - Get platform capabilities",
            "/health": "GET - Health check"
        }
    }


@app.get("/capabilities")
async def get_capabilities():
    """Get platform capabilities"""
    return engine.get_capabilities()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AgenticAP",
        "capabilities": {
            "read": True,
            "reason": True,
            "reconcile": True
        }
    }


@app.post("/process", response_model=ProcessingResponse)
async def process_invoice(
    file: UploadFile = File(...),
    reference_data: Optional[str] = None
):
    """
    Process an invoice document with READ, REASON, and RECONCILE capabilities
    
    Args:
        file: Invoice document file (PDF, PNG, JPG, etc.)
        reference_data: Optional JSON string with reference data for reconciliation
        
    Returns:
        Processing results including analysis and reconciliation
    """
    logger.info(f"Processing uploaded file: {file.filename}")
    
    # Save uploaded file to temporary location
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Parse reference data if provided
        ref_data = None
        if reference_data:
            import json
            try:
                ref_data = json.loads(reference_data)
            except json.JSONDecodeError:
                logger.warning("Invalid reference data JSON, processing without reconciliation")
        
        # Process the invoice
        result = engine.process_invoice(tmp_path, ref_data)
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        if result['success']:
            return ProcessingResponse(
                success=True,
                file_name=file.filename,
                analysis=result['analysis'],
                reconciliation=result.get('reconciliation'),
                overall_confidence=result['overall_confidence']
            )
        else:
            return ProcessingResponse(
                success=False,
                file_name=file.filename,
                error=result.get('error', 'Unknown error')
            )
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process_with_reference")
async def process_with_reference(
    file: UploadFile = File(...),
    reference: ReferenceData = None
):
    """
    Process an invoice with structured reference data for reconciliation
    
    Args:
        file: Invoice document file
        reference: Structured reference data
        
    Returns:
        Processing results
    """
    logger.info(f"Processing file with reference data: {file.filename}")
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Convert reference data to dict
        ref_data = reference.dict(exclude_none=True) if reference else None
        
        # Process the invoice
        result = engine.process_invoice(tmp_path, ref_data)
        
        # Clean up
        os.unlink(tmp_path)
        
        return result
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
