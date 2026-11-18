"""Reads and writes on the `chunks` collection in Firestore."""

from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector

from sage.config import get_app_config
from sage.domain.qa.models import Chunk
from sage.integrations.firestore.client import get_firestore_client


def find_nearest_chunks(embedding: list[float]) -> list[Chunk]:
    config = get_app_config()
    db = get_firestore_client()
    collection = db.collection(config.firestore_collection)
    vector_query = collection.find_nearest(
        vector_field="embedding",
        query_vector=Vector(embedding),
        distance_measure=DistanceMeasure.COSINE,
        limit=config.top_k,
    )
    chunks: list[Chunk] = []
    for doc in vector_query.stream():
        data = doc.to_dict() or {}
        chunks.append(
            Chunk(
                id=doc.id,
                text=data.get("text", ""),
                source=data.get("source", ""),
                section=data.get("section"),
                chunk_index=int(data.get("chunk_index", 0)),
            )
        )
    return chunks


def delete_chunks_for_source(source: str) -> None:
    """Remove existing chunks for a document, so re-running the ingestion script is safe."""
    config = get_app_config()
    db = get_firestore_client()
    docs = db.collection(config.firestore_collection).where("source", "==", source).stream()
    for doc in docs:
        doc.reference.delete()


def add_chunk(
    chunk_id: str,
    text: str,
    embedding: list[float],
    source: str,
    section: str | None,
    chunk_index: int,
) -> None:
    config = get_app_config()
    db = get_firestore_client()
    db.collection(config.firestore_collection).document(chunk_id).set(
        {
            "text": text,
            "embedding": Vector(embedding),
            "source": source,
            "section": section,
            "chunk_index": chunk_index,
        }
    ) 