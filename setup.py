"""Setup script for AgenticAP package"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="agentic_ap",
    version="1.0.0",
    author="AgenticAP Team",
    description="AI-native financial automation platform with READ, REASON, and RECONCILE capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williamjxj/AgenticAP",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "transformers>=4.35.0",
        "torch>=2.1.0",
        "langchain>=0.1.0",
        "langchain-community>=0.0.10",
        "pypdf2>=3.0.0",
        "pdf2image>=1.16.3",
        "pillow>=10.1.0",
        "python-docx>=1.1.0",
        "pytesseract>=0.3.10",
        "easyocr>=1.7.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agentic-ap=agentic_ap.api.main:main",
        ],
    },
)
