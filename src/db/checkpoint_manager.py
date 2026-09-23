import sqlite3
import os
from src.config import config
from src.logger import log
from src.exceptions import CheckpointError

class CheckpointManager:
    """Manages SQLite database for saving generation states (checkpoints)."""
    
    def __init__(self):
        self.db_path = config.DATABASE_PATH
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._initialize_db()
        
    def _initialize_db(self):
        """Creates the necessary tables if they don't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS checkpoints (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_name TEXT UNIQUE,
                        idea_outline TEXT,
                        lit_review TEXT,
                        refined_text TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
                log.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            raise CheckpointError(f"Failed to initialize DB: {str(e)}")
            
    def save_checkpoint(self, project_name: str, key: str, value: str):
        """Saves a specific section to the project's checkpoint."""
        valid_keys = ['idea_outline', 'lit_review', 'refined_text']
        if key not in valid_keys:
            raise ValueError(f"Invalid checkpoint key. Must be one of {valid_keys}")
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if project exists
                cursor.execute("SELECT id FROM checkpoints WHERE project_name = ?", (project_name,))
                result = cursor.fetchone()
                
                if result:
                    # Update
                    cursor.execute(f"UPDATE checkpoints SET {key} = ? WHERE project_name = ?", (value, project_name))
                else:
                    # Insert
                    cursor.execute(f"INSERT INTO checkpoints (project_name, {key}) VALUES (?, ?)", (project_name, value))
                
                conn.commit()
                log.info(f"Checkpoint saved for project '{project_name}', key: '{key}'")
        except Exception as e:
            raise CheckpointError(f"Failed to save checkpoint: {str(e)}")
            
    def load_checkpoint(self, project_name: str) -> dict:
        """Loads all data for a specific project."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM checkpoints WHERE project_name = ?", (project_name,))
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return {}
        except Exception as e:
            raise CheckpointError(f"Failed to load checkpoint: {str(e)}")
