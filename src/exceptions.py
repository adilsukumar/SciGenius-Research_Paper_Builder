class SciGeniusError(Exception):
    """Base exception for all SciGenius errors."""
    pass

class ConfigurationError(SciGeniusError):
    """Raised when there is an issue with the configuration (e.g., missing API key)."""
    pass

class IngestionError(SciGeniusError):
    """Raised when there is an issue parsing a PDF or extracting text."""
    pass

class GenerationError(SciGeniusError):
    """Raised when the LLM fails to generate output or hits rate limits."""
    pass

class CheckpointError(SciGeniusError):
    """Raised when there is an issue saving or loading state from the database."""
    pass
