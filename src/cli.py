import sys
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import track
import time

from src.config import config
from src.logger import log
from src.exceptions import ConfigurationError, GenerationError
from src.graph.pdf_parser import PDFParser
from src.graph.ner_engine import NEREngine
from src.graph.relation_extractor import RelationExtractor
from src.graph.builder import GraphBuilder
from src.generation.idea_expander import IdeaExpander
from src.generation.lit_review import LiteratureReviewGenerator
from src.generation.style_editor import StyleEditor
from src.db.checkpoint_manager import CheckpointManager
from src.export.formatter import Formatter

console = Console()

class SciGeniusCLI:
    """The interactive command-line interface for SciGenius."""
    
    def __init__(self):
        console.print(Panel.fit("[bold blue]SciGenius[/bold blue] 🧠\n[italic]Literature mapping and drafting assistant[/italic]"))
        self.db = CheckpointManager()
        
    def check_setup(self):
        """Validates configuration."""
        try:
            config.validate()
        except ConfigurationError as e:
            console.print(f"[bold red]Configuration Error:[/bold red] {str(e)}")
            sys.exit(1)
            
    def run(self):
        """Main execution flow."""
        self.check_setup()
        
        project_name = Prompt.ask("Enter a name for this research project")
        project_data = self.db.load_checkpoint(project_name)
        
        if project_data:
            console.print(f"[green]Found existing checkpoint for '{project_name}'![/green]")
            resume = Prompt.ask("Do you want to resume from the checkpoint?", choices=["y", "n"], default="y")
            if resume == 'n':
                project_data = {}
        
        # Step 1: Idea Expansion
        if not project_data.get('idea_outline'):
            console.print("\n[bold cyan]--- Step 1: Idea Generation ---[/bold cyan]")
            user_idea = Prompt.ask("Describe your research idea (brief or detailed)")
            
            with console.status("[bold green]Expanding idea into a full academic outline...[/bold green]"):
                expander = IdeaExpander()
                outline = expander.expand(user_idea)
                
            self.db.save_checkpoint(project_name, "idea_outline", outline)
            console.print(Panel(outline, title="Generated Outline", expand=False))
        else:
            console.print("[cyan]Skipping Step 1 (Loaded from checkpoint)[/cyan]")
            outline = project_data['idea_outline']
            
        # Step 2: Knowledge Graph Ingestion
        console.print("\n[bold cyan]--- Step 2: Knowledge Graph Ingestion ---[/bold cyan]")
        pdf_path = Prompt.ask("Enter the path to a reference PDF for the Literature Review (or press Enter to skip)", default="")
        graph_summary = "No reference papers provided."
        
        if pdf_path and os.path.exists(pdf_path):
            with console.status("[bold green]Ingesting PDF and building Knowledge Graph...[/bold green]"):
                text = PDFParser.extract_text(pdf_path)
                
                ner = NEREngine()
                entities = ner.extract_entities(text[:50000]) # Limit to first 50k chars for speed
                
                rel_extractor = RelationExtractor()
                relations = rel_extractor.extract_relations(text[:50000], entities)
                
                builder = GraphBuilder()
                builder.build(entities, relations)
                graph_summary = builder.get_summary()
                console.print(f"[green]Knowledge Graph built successfully![/green]")
                
        # Step 3: Literature Review
        if not project_data.get('lit_review'):
            console.print("\n[bold cyan]--- Step 3: Literature Review Generation ---[/bold cyan]")
            
            with console.status("[bold green]Writing Literature Review based on Knowledge Graph...[/bold green]"):
                lit_gen = LiteratureReviewGenerator()
                lit_review_draft = lit_gen.generate(project_name, graph_summary)
            
            # Step 4: clarity and style edit
            with console.status("[bold green]Editing the draft for clarity and consistency...[/bold green]"):
                editor = StyleEditor()
                final_lit_review = editor.edit(lit_review_draft)
                
            self.db.save_checkpoint(project_name, "lit_review", final_lit_review)
            console.print("[green]Draft generated. Verify every claim and citation before use.[/green]")
        else:
            console.print("[cyan]Skipping Step 3 (Loaded from checkpoint)[/cyan]")
            final_lit_review = project_data['lit_review']
            
        # Step 5: Export
        console.print("\n[bold cyan]--- Step 5: Exporting Paper ---[/bold cyan]")
        export_path = f"data/exports/{project_name}.md"
        Formatter.export_to_markdown(project_name, outline, final_lit_review, export_path)
        console.print(f"[bold green]🎉 Project completed! Exported to: {export_path}[/bold green]")
        
if __name__ == "__main__":
    cli = SciGeniusCLI()
    cli.run()
