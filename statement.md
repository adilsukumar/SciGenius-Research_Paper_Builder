# Problem Statement: Automated Literature Synthesis and AI-Detection Evasion in Academic Writing

## Scope
The project focuses on creating a CLI-based tool (SciGenius) that bridges the gap between raw unstructured PDF literature and highly structured, human-readable academic drafts. The system employs NLP to build a Knowledge Graph from literature, and then utilizes an LLM to expand user concepts and synthesize the graph into a literature review. Crucially, a "Humanizer" module applies specific prompting constraints to lower the predictability (perplexity) of the text, helping it mimic human academic writing.

## Target Users
- **Graduate Students & PhD Candidates:** Looking to rapidly synthesize dozens of papers into a coherent literature review.
- **Academic Researchers:** Needing to structure raw ideas into formatted IEEE outlines.
- **Developers:** Interested in Retrieval-Augmented Generation (RAG) and Graph-based LLM architectures.

## High-Level Features
1. **PDF Text Extraction & Cleaning**
2. **Named Entity Recognition (NER) & Relation Extraction**
3. **NetworkX Knowledge Graph Construction**
4. **LLM-Powered Idea Expansion (Gemini 1.5 Pro)**
5. **Context-Aware Literature Review Generation**
6. **Perplexity-Busting Text Humanization**
7. **SQLite-based Checkpointing & Session Management**
8. **Interactive Terminal UI (Rich)**
