"""Vector database integration for semantic search"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from helix.utils.logger import get_logger

logger = get_logger(__name__)


class VectorDatabase(ABC):
    """Abstract base class for vector databases"""

    @abstractmethod
    async def add_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, Any]]) -> None:
        """Add vectors to the database"""
        pass

    @abstractmethod
    async def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        pass

    @abstractmethod
    async def delete(self, ids: List[str]) -> None:
        """Delete vectors by ID"""
        pass


class ChromaVectorDB(VectorDatabase):
    """Chroma vector database implementation"""

    def __init__(self, collection_name: str = "helix_embeddings"):
        try:
            import chromadb
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Chroma collection initialized: {collection_name}")
        except ImportError:
            raise ImportError("chromadb is required for vector storage")

    async def add_vectors(
        self,
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> None:
        """Add vectors to Chroma collection"""
        if ids is None:
            ids = [f"id_{i}" for i in range(len(vectors))]

        try:
            self.collection.add(
                ids=ids,
                embeddings=vectors,
                metadatas=metadata
            )
            logger.debug(f"Added {len(vectors)} vectors to collection")
        except Exception as e:
            logger.error(f"Error adding vectors: {e}")
            raise

    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        try:
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=top_k
            )
            return results
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            return []

    async def delete(self, ids: List[str]) -> None:
        """Delete vectors from collection"""
        try:
            self.collection.delete(ids=ids)
            logger.debug(f"Deleted {len(ids)} vectors")
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            raise

    def clear(self) -> None:
        """Clear entire collection"""
        try:
            self.client.delete_collection(name=self.collection.name)
            logger.info(f"Cleared collection: {self.collection.name}")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
