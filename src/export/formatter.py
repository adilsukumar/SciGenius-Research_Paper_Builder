import os
from src.logger import log

class Formatter:
    """Formats the generated text into standard formats (Markdown/LaTeX)."""
    
    @staticmethod
    def export_to_markdown(title: str, outline: str, lit_review: str, filepath: str):
        """Exports the research paper to a Markdown file."""
        log.info(f"Exporting to Markdown: {filepath}")
        
        # Ensure dir exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        content = f"# {title}\n\n"
        content += "## Outline & Methodology\n\n"
        content += f"{outline}\n\n"
        content += "---\n\n"
        content += "## Background and Related Work (Literature Review)\n\n"
        content += f"{lit_review}\n\n"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        log.info("Export complete.")
