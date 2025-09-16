<<<<<<< HEAD
# Field Note Extraction API

This project provides a powerful, AI-driven API to automatically extract structured data from images of construction field notes. It uses modern machine learning models to perform Optical Character Recognition (OCR) and intelligent information extraction, converting unstructured images into clean, usable JSON data.

## Key Features

-   **AI-Powered Extraction**: Leverages Large Language Models (LLMs) via LangChain for high-accuracy data extraction.
-   **Multiple Document Types**: Supports different field note formats with dedicated endpoints:
    -   Concrete Delivery Notes
    -   General Materials Delivery Notes (e.g., soil, sand, paint, etc.)
-   **RESTful API**: Built with FastAPI for a modern, high-performance, and easy-to-use interface.
-   **Asynchronous Processing**: Non-blocking I/O for efficient handling of image downloads and model inference.
-   **Input Validation**: Securely handles image URLs, validating content type and file size before processing.
-   **Structured JSON Output**: Returns predictable and well-structured JSON, perfect for database ingestion or further processing.

## Technology Stack

-   **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Web Server**: [Uvicorn](https://www.uvicorn.org/)
-   **AI / LLM Orchestration**: [LangChain](https://www.langchain.com/)
-   **Data Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/)
-   **HTTP Client**: [HTTPX](https://www.python-httpx.org/)
-   **Image Processing**: [Pillow](https://python-pillow.org/)

## Setup and Installation

### 1. Prerequisites

-   Python 3.9+
-   `pip` and `venv`

### 2. Clone the Repository

```bash
git clone https://github.com/truonggiang1757/field_note.git
cd field_note
=======
# field_note
>>>>>>> de3fd0d40dc4cbeafffe6b101a83cba497700250
