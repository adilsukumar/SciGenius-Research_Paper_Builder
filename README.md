# SciGenius 🧠
**Automated Knowledge Graph & Humanized Research Paper Generator**

## Overview
SciGenius is an advanced, multi-modal AI system built to automate the heavy lifting of academic research. It ingests source PDFs, builds a Semantic Knowledge Graph using Natural Language Processing (NLP), and uses state-of-the-art LLMs (Gemini 1.5 Pro) to generate IEEE-grade, humanized research outlines and literature reviews.

## Features
- **Knowledge Graph Generation:** Extracts Entities (NER) and Relations from PDFs using `spaCy` and `NetworkX`.
- **Idea Expansion:** Turns a 1-sentence prompt into a full academic research outline.
- **Humanizer Engine:** Bypasses AI detection by injecting burstiness, perplexity, and stylistic variation.
- **Stateful Execution:** Uses a local SQLite database to checkpoint progress, meaning you never lose work if an API fails.
- **Beautiful CLI:** Built with `rich` for an interactive, wizard-like terminal experience.

## Technologies Used
- `Python 3.10+`
- `google-generativeai` (Gemini API)
- `spaCy` (NLP)
- `NetworkX` (Graph building)
- `SQLite` (Checkpoints)
- `Rich` (CLI interface)

## Installation & Setup

1. **Clone the repository**
2. **Set up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
4. **Configure Environment:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage
Run the CLI wizard:
```bash
python -m src.cli
```

Follow the on-screen prompts to input your research idea and path to any reference PDFs. The output will be saved in `data/exports/`.

## Testing
Run the unit test suite using `pytest`:
```bash
pytest tests/
```
