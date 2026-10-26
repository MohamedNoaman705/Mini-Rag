from stores.llm.LLMInterface import LLMInterface
import ollama
from typing import Optional, List
from ..LLMEnums import OllamaEnum
import logging


class OllamaProvider(LLMInterface):

    def __init__(self, api_url: Optional[str],
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):

        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.enums = OllamaEnum
        # Use a bound client so the custom host is actually respected.
        self.client = ollama.Client(host=self.api_url)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: List[dict] = None,
                       max_output_token: Optional[int] = None,
                       temperature: Optional[float] = None):
        if not self.generation_model_id:
            self.logger.error("Ollama generation model not set")
            return None

        max_output_token = max_output_token if max_output_token is not None else self.default_generation_max_output_tokens
        temperature = temperature if temperature is not None else self.default_generation_temperature

        # Don't mutate the caller's list.
        chat_history = list(chat_history) if chat_history else []
        chat_history.append(
            self.construct_prompt(
                prompt=prompt,
                role=OllamaEnum.USER.value
            )
        )

        try:
            response = self.client.chat(
                model=self.generation_model_id,
                messages=chat_history,
                options={
                    "num_predict": max_output_token,
                    "temperature": temperature,
                }
            )
        except Exception as e:
            self.logger.error(f"Error communicating with Ollama server: {e}")
            return None

        if not response or not response.get("message") or not response["message"].get("content"):
            self.logger.error("Error while generating response from Ollama")
            return None

        return response["message"]["content"]

    def embed_text(self, text: str, document_type: Optional[str] = None):
        if not self.embedding_model_id:
            self.logger.error("Ollama embedding model not set")
            return None

        processed_text = self.process_text(text)

        try:
            response = self.client.embeddings(
                model=self.embedding_model_id,
                prompt=processed_text
            )
        except Exception as e:
            self.logger.error(f"Error generating embeddings with Ollama: {e}")
            return None

        if not response or not response.get("embedding"):
            self.logger.error("Ollama embedding response is empty or invalid")
            return None

        return response["embedding"]

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": prompt
        }
