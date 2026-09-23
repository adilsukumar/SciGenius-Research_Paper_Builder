# Problem statement: traceable literature mapping and assisted synthesis

Researchers often begin with a set of PDFs whose terminology, entities, and relationships are difficult to compare quickly. SciGenius investigates whether a lightweight NLP and graph pipeline can make those relationships easier to inspect before a researcher writes a synthesis.

The system extracts text from authorised source PDFs, identifies candidate entities and relations, stores them in a graph, and provides the resulting context to a language model. The model produces a provisional outline or literature-review draft. A separate editing stage improves clarity while explicitly preserving claims, citations, uncertainty, and technical meaning.

The tool is designed around human review. It does not establish the truth of an extracted relation, perform a systematic review, or make generated prose publication-ready. Every output must be checked against the original sources, and AI assistance should be disclosed wherever required.

## Engineering objectives

1. Parse research PDFs and retain source provenance.
2. Extract domain entities and candidate relationships.
3. Represent literature structure with NetworkX.
4. Generate source-constrained, explicitly provisional drafts.
5. Checkpoint multi-stage work in SQLite.
6. Export drafts for researcher revision rather than automatic submission.

## Evaluation priorities

Future evaluation should measure entity/relation precision and recall, provenance coverage, unsupported-claim rate, and usefulness to researchers. These measures are more meaningful than whether generated prose merely appears polished.
