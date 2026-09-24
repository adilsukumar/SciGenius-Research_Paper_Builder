from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil

from src.config import config
from src.exceptions import ConfigurationError, GenerationError
from src.graph.pdf_parser import PDFParser
from src.graph.ner_engine import NEREngine
from src.graph.relation_extractor import RelationExtractor
from src.graph.builder import GraphBuilder
from src.generation.idea_expander import IdeaExpander
from src.generation.lit_review import LiteratureReviewGenerator
from src.generation.humanizer_engine import HumanizerEngine
from src.db.checkpoint_manager import CheckpointManager
from src.export.formatter import Formatter
from src.logger import log

app = FastAPI(title="SciGenius API")

# Allow CORS for the Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = CheckpointManager()

# Pydantic Models
class ProjectRequest(BaseModel):
    project_name: str

class IdeaRequest(BaseModel):
    project_name: str
    idea: str

class GenerateRequest(BaseModel):
    project_name: str
    
@app.on_event("startup")
def startup_event():
    try:
        config.validate()
    except ConfigurationError as e:
        log.error(f"Config error on startup: {e}")

@app.post("/api/project")
def init_project(req: ProjectRequest):
    data = db.load_checkpoint(req.project_name)
    return {"status": "success", "project_name": req.project_name, "data": data}

@app.post("/api/expand")
def expand_idea(req: IdeaRequest):
    try:
        expander = IdeaExpander()
        outline = expander.expand(req.idea)
        db.save_checkpoint(req.project_name, "idea_outline", outline)
        return {"status": "success", "outline": outline}
    except GenerationError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ingest")
async def ingest_pdf(project_name: str = Form(...), file: UploadFile = File(...)):
    try:
        # Save file temporarily
        upload_dir = "/tmp/uploads" if os.getenv("VERCEL") == "1" else "data/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = f"{upload_dir}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process PDF
        text = PDFParser.extract_text(file_path)
        ner = NEREngine()
        entities = ner.extract_entities(text[:50000]) 
        rel_extractor = RelationExtractor()
        relations = rel_extractor.extract_relations(text[:50000], entities)
        builder = GraphBuilder()
        builder.build(entities, relations)
        graph_summary = builder.get_summary()
        
        # We don't save graph_summary to SQLite in this basic version, we can just return it or save to a file
        summary_path = f"{upload_dir}/{project_name}_graph.txt"
        with open(summary_path, "w") as f:
            f.write(graph_summary)
            
        return {"status": "success", "graph_summary": graph_summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/humanize")
def generate_and_humanize(req: GenerateRequest):
    try:
        project_data = db.load_checkpoint(req.project_name)
        
        upload_dir = "/tmp/uploads" if os.getenv("VERCEL") == "1" else "data/uploads"
        summary_path = f"{upload_dir}/{req.project_name}_graph.txt"
        graph_summary = ""
        if os.path.exists(summary_path):
            with open(summary_path, "r") as f:
                graph_summary = f.read()
                
        lit_gen = LiteratureReviewGenerator()
        lit_review_draft = lit_gen.generate(req.project_name, graph_summary)
        
        humanizer = HumanizerEngine()
        final_lit_review = humanizer.humanize(lit_review_draft)
        
        db.save_checkpoint(req.project_name, "lit_review", final_lit_review)
        
        # Export automatically
        export_dir = "/tmp/exports" if os.getenv("VERCEL") == "1" else "data/exports"
        os.makedirs(export_dir, exist_ok=True)
        outline = project_data.get("idea_outline", "")
        export_path = f"{export_dir}/{req.project_name}.md"
        Formatter.export_to_markdown(req.project_name, outline, final_lit_review, export_path)
        
        return {"status": "success", "lit_review": final_lit_review, "export_path": export_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
