# Sentence Profiler

A full-stack web application designed to analyze text for sentence length and grammatical complexity (T-unit analysis).

## Features
- **Text Analysis**: Real-time grammatical decomposition.
- **File Support**: Upload `.txt`, `.docx`, and `.pdf` files.
- **Dynamic Frontend**: Modern UI with real-time feedback.
- **Modular Backend**: Built with FastAPI and spaCy.

## Project Structure
- `frontend/`: HTML, CSS, and JS files.
- `backend/`: FastAPI server and linguistic analysis modules.
- `requirements.txt`: Python dependencies.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Download spaCy model: `python -m spacy download en_core_web_sm`
3. Run backend: `python backend/main.py`
4. Open `frontend/index.html` in your browser.
