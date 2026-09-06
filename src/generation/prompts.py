HUMANIZE_PROMPT = """
You are an expert academic researcher writing a paper for a prestigious IEEE/Scopus journal.
Your task is to take the following AI-generated draft and rewrite it to sound completely human, bypassing AI detection systems like Turnitin or GPTZero.

CRITICAL INSTRUCTIONS FOR HUMANIZATION:
1. **Vary Sentence Structure**: Use a mix of short, punchy sentences and longer, complex sentences. AI text is typically too uniform in sentence length.
2. **Increase Perplexity**: Use less predictable word choices. Avoid common AI phrases like "In conclusion," "It is important to note that," "Delving into," or "A tapestry of".
3. **Burstiness**: Humans write in bursts. Sometimes they string together several short clauses; other times they write a very long, flowing sentence. Mimic this.
4. **Academic Tone**: Maintain a highly rigorous, objective, and scholarly tone suitable for an IEEE/Scopus journal.
5. **No AI Signatures**: Do not apologize, do not say "As an AI", just output the rewritten text.

Original Draft:
{draft}

Rewritten Humanized Section:
"""

IDEA_EXPANSION_PROMPT = """
You are a brilliant PhD advisor in Computer Science/Engineering. A student has come to you with a rough idea for a research paper. 
Your task is to expand this brief idea into a comprehensive, robust research outline suitable for a top-tier journal.

Student's Idea:
{idea}

Please output a structured outline including:
1. Proposed Title (Catchy and academic)
2. Abstract (A 250-word summary of the proposed innovation)
3. Problem Statement (Clear and concise)
4. Proposed Methodology (High-level architecture or approach)
5. Expected Contributions (Why this is novel)
"""

LIT_REVIEW_PROMPT = """
You are an expert researcher writing the "Background and Related Work" section of an IEEE paper.
You have been provided with a Knowledge Graph summary extracted from various source papers and PDFs.

Knowledge Graph Context:
{graph_summary}

Research Topic:
{topic}

Task:
Write a comprehensive 500-word Literature Review. Synthesize the concepts and relationships from the Knowledge Graph. Highlight the gaps in the current literature that our research topic addresses.
Do NOT simply list the concepts. Weave them into a cohesive academic narrative.
"""
