from enum import Enum

class ResponseSignal(Enum):


    FILE_VALIDATED_SUCCESSFULLY = "File validated successfully"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_TOO_LARGE = "File size too large"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    FILE_UPLOADED_FAILED = "File uploaded failed"

    PROCESSING_FAILED = "Processing failed"
    PROCESSING_SUCCESSFULLY = "Processing successfully"

    NO_FILES_ERROR = "No files found"
    FILE_ID_ERROR = "No file id found"

    PROJECT_NOT_FOUND = "Project not found"
    INSERT_INTO_VECTORDB_ERROR = "Insert in vectordb failed"
    INSERT_INTO_VECTORDB_SUCCESSFULLY = "Insert in vectordb successfully"
    VECTOR_DB_COLLECTION_RETRIEVED = "VECTOR DB collection retrieved"
    VECTOR_DB_SEARCH_ERROR = "VECTOR DB search failed"
    VECTOR_DB_SEARCH_SUCCESSFULLY = "VECTOR DB search successfully"

    RAG_ANSWER_ERROR = "Rag answer failed"
    RAG_ANSWER_SUCCESSFULLY = "Rag answer successfully"