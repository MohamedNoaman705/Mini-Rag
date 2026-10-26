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

class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"