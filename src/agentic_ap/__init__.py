"""
AgenticAP - AI-native financial automation platform
Built on open-source stack for cost-effective document processing
"""

__version__ = "1.0.0"
__author__ = "AgenticAP Team"

from .core.agentic_engine import AgenticEngine
from .core.document_reader import DocumentReader
from .core.reasoning_engine import ReasoningEngine
from .core.reconciliation_engine import ReconciliationEngine

__all__ = [
    "AgenticEngine",
    "DocumentReader", 
    "ReasoningEngine",
    "ReconciliationEngine",
]
