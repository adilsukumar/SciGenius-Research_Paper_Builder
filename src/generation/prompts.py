STYLE_EDIT_PROMPT = """
You are editing an academic draft for clarity, precision, and readability.

Requirements:
1. Preserve the author's claims, qualifications, citations, and technical meaning.
2. Do not invent evidence, references, numerical results, or methods.
3. Prefer direct language and remove repetition or unsupported emphasis.
4. Keep uncertainty explicit and distinguish source findings from the author's interpretation.
5. Return only the revised draft. The researcher will verify it against the source material and disclose AI assistance where required by their institution or publisher.

Original Draft:
{draft}

Revised Draft:
"""

IDEA_EXPANSION_PROMPT = """
You are helping a researcher turn an early idea into a structured outline for critical review.
Do not claim novelty, results, or references that have not been supplied.

Student's Idea:
{idea}

Please output a structured outline including:
1. Working Title
2. Draft Abstract (clearly framed as a proposal, not completed research)
3. Problem Statement (Clear and concise)
4. Proposed Methodology (High-level architecture or approach)
5. Proposed Contributions and assumptions that still need validation
"""

LIT_REVIEW_PROMPT = """
You are an expert researcher writing the "Background and Related Work" section of an IEEE paper.
You have been provided with a Knowledge Graph summary extracted from various source papers and PDFs.

Knowledge Graph Context:
{graph_summary}

Research Topic:
{topic}

Task:
Draft a literature-review section of up to 500 words using only the supplied graph context. Synthesize relationships rather than listing concepts. Clearly flag missing evidence and do not fabricate citations, findings, or research gaps.
"""
