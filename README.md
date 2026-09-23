# SciGenius

An experimental literature-mapping and drafting assistant that turns uploaded research PDFs into a small semantic knowledge graph and a reviewable literature-summary draft.

SciGenius explores how named-entity recognition, relation extraction, graph structures, and language models can support—rather than replace—the careful work of reading and synthesis.

## Workflow

1. Expand an early research question into a provisional outline.
2. Extract text from a reference PDF.
3. Identify entities and candidate relations with spaCy.
4. Represent the extracted relationships as a NetworkX graph.
5. Generate a literature-review draft grounded in the graph summary.
6. Edit the draft for clarity while preserving claims and qualifications.
7. Save checkpoints locally and export a Markdown draft.

## Responsible-use principles

- Generated text is a draft, not evidence.
- The researcher must verify every claim and citation against the original sources.
- The system is instructed not to invent results, references, novelty, or research gaps.
- Users remain responsible for authorship and for following their institution's or publisher's AI-disclosure policy.
- SciGenius is not designed to evade plagiarism or AI-detection systems.

## Technology

Python · FastAPI · spaCy · NetworkX · SQLite · Rich · Vite · JavaScript

The language-model client supports Cohere and OpenAI-compatible REST APIs through environment configuration.

## Setup

```bash
git clone https://github.com/AdilSukumar/SciGenius-Research_Paper_Builder.git
cd SciGenius-Research_Paper_Builder
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Copy `.env.example` to `.env` and configure the language-model endpoint. Never commit credentials.

## Run

CLI:

```bash
python -m src.cli
```

API:

```bash
uvicorn src.api:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Test

```bash
pytest
```

## Current limitations

- Entity and relation quality depends heavily on PDF extraction and the general-purpose NLP model.
- The current graph summary is lightweight and does not constitute a systematic review.
- Source provenance is not yet preserved at sentence level in generated drafts.
- LLM output can still contain unsupported statements; human verification is mandatory.
- Uploaded PDFs should contain material the user is authorised to process.

## Next steps

- Preserve page- and sentence-level provenance for every graph edge.
- Require evidence links for generated claims.
- Add multi-document deduplication and contradiction detection.
- Evaluate extraction precision/recall on a labelled corpus.
- Add tests for upload validation, project-name sanitisation, and API failure modes.
