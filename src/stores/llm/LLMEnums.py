from enum import Enum
from xml.dom.minidom import DocumentType


class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    OLLAMA = "OLLAMA"

class OpenAIEnum(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "ASSISTANT"

class OllamaEnum(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

    DEFAULT_GENERATION_MODEL = "llama3"
    DEFAULT_EMBEDDING_MODEL = "nomic-embed-text"

    DEFAULT_API_URL = "http://localhost:11434"

class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"