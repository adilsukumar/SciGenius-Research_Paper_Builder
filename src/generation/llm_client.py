import requests
from src.config import config
from src.exceptions import GenerationError
from src.logger import log

class LLMClient:
    """Wrapper for OpenAI-compatible and Cohere REST APIs."""
    
    def __init__(self):
        config.validate()
        self.api_key = config.LLM_API_KEY
        self.base_url = config.LLM_BASE_URL
        self.model = config.LLM_MODEL
        
    def generate_text(self, prompt: str, temperature: float = None) -> str:
        """Sends a prompt to the LLM and returns the response."""
        temp = temperature if temperature is not None else config.TEMPERATURE
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Checking if it's Cohere vs OpenAI compatible by URL
        is_cohere = "cohere" in self.base_url.lower()
        
        if is_cohere:
            payload = {
                "model": self.model,
                "message": prompt,
                "temperature": temp,
                "max_tokens": config.MAX_TOKENS
            }
        else:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temp,
                "max_tokens": config.MAX_TOKENS
            }
            
        try:
            log.info(f"Sending request to LLM API ({self.model})...")
            response = requests.post(self.base_url, json=payload, headers=headers)
            
            if response.status_code != 200:
                raise GenerationError(f"API Error {response.status_code}: {response.text}")
                
            data = response.json()
            
            if is_cohere:
                return data.get("text", "")
            else:
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
                
        except Exception as e:
            log.error(f"LLM API Error: {str(e)}")
            raise GenerationError(f"Failed to generate text: {str(e)}")
