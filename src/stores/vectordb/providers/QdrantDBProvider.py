from typing import Optional
import logging
import uuid
from qdrant_client import QdrantClient, models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
from models.db_schemes import RetrievedDocument


class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_path: str, distance_method: str):
        self.client = None
        self.db_path = db_path
        self.distance_method = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_exist(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self) -> list:
        return self.client.list_collection_names()

    def get_collection_info(self, collection_name: str):
        if not self.is_collection_exist(collection_name=collection_name):
            return None

        collection_info = self.client.get_collection(collection_name=collection_name)

        # Safely convert Pydantic model response to dict if available
        # if hasattr(collection_info, "model_dump"):
        #     return collection_info.model_dump()
        # elif hasattr(collection_info, "dict"):
        #     return collection_info.dict()

        return collection_info

    def delete_collection(self, collection_name: str):
        if self.is_collection_exist(collection_name=collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        return None

    def create_collection(
        self,
        collection_name: str,
        embedding_size: int,
        do_reset: bool = False,
    ):
        if do_reset:
            _ = self.delete_collection(collection_name=collection_name)

        if not self.is_collection_exist(collection_name=collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size, distance=self.distance_method
                ),
            )
            return True

        return False

    def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: Optional[dict] = None,
        record_id: Optional[str] = None,
    ):
        if not self.is_collection_exist(collection_name=collection_name):
            self.logger.debug(f"Collection {collection_name} does not exist")
            return False

        # Generate a unique string ID if not provided
        if not record_id:
            record_id = str(uuid.uuid4())

        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=record_id,
                        vector=vector,
                        payload={"text": text, "metadata": metadata},
                    )
                ],
            )
        except Exception as e:
            self.logger.error(f"Failed to upload record: {e}")
            return False
        return True

    def insert_many(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: Optional[list] = None,
        record_ids: Optional[list] = None,
        batch_size: int = 50,
    ):
        if not self.is_collection_exist(collection_name=collection_name):
            self.logger.debug(f"Collection {collection_name} does not exist")
            return False

        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = [None] * len(texts)

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size
            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            batch_records = [
                models.Record(
                    id=(
                        batch_record_ids[x]
                        if batch_record_ids[x] is not None
                        else str(uuid.uuid4())
                    ),
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x],
                        "metadata": batch_metadata[x],
                    },
                )
                for x in range(len(batch_texts))
            ]
            try:
                _ = self.client.upload_records(
                    collection_name=collection_name, records=batch_records
                )
            except Exception as e:
                self.logger.error(f"Failed to upload records: {e}")
                return False

        return True

    def search_by_vector(
        self, collection_name: str, vector: list, limit: int = 5):

        results = self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )

        if not results or len(results) == 0:
            return None

        return [
            RetrievedDocument(**{
                "score": result.score,
                "text": result.payload["text"],
            })
            for result in results
        ]