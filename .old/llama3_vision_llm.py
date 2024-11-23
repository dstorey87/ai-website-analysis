import requests
from langchain.llms.base import LLM
from typing import Optional, List
from pydantic import BaseModel
import json  # Add this import at the top of your file

class Llama3VisionLLM(LLM, BaseModel):
    """Custom LLM wrapper for the Llama 3.2 Vision model via Ollama."""

    model_name: str = "llama3.2-vision"
    host: str = "http://localhost:11434"

    @property
    def _llm_type(self) -> str:
        return "llama3_vision"



    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Send a prompt to the Llama 3.2 Vision model via Ollama with streaming support."""
        url = f"{self.host}/api/generate"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model_name,
            "prompt": prompt
        }

        response = requests.post(url, json=payload, headers=headers, stream=True)

        if response.status_code != 200:
            raise ValueError(f"Error from Ollama API: {response.text}")

        # Process the streamed response
        result = []
        for line in response.iter_lines():
            if line:
                try:
                    # Use json.loads from the built-in json module
                    chunk = json.loads(line.decode("utf-8"))
                    result.append(chunk.get("response", ""))
                except Exception as e:
                    print(f"Failed to parse chunk: {line.decode('utf-8')}")
                    raise e

        # Join all chunks into a single response
        return "".join(result)

