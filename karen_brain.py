import requests
import json

class KarenBrain:
    def __init__(self, model_name="phi4-mini"):
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/generate"

    def chat_offline(self, prompt):
        system_instruction = "You are KAREN, an advanced local desktop assistant. You must ALWAYS reply in clear, concise English. Never switch languages."
        full_prompt = f"{system_instruction}\nUser: {prompt}\nKaren:"

        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=(3.0, 30.0))
            if response.status_code == 200:
                return response.json().get("response", "No response generated.").strip()
            else:
                return f"[Error] Ollama responded with status code {response.status_code}"
        except requests.exceptions.ConnectionError:
            return "[Error] Could not connect to Ollama. Make sure Ollama is running locally."
        except requests.exceptions.Timeout:
            return "[Error] Ollama request timed out."
        except Exception as e:
            return f"[Error] {str(e)}"