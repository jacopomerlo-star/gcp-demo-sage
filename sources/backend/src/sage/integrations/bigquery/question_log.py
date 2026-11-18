"""Writes one row per question to BigQuery for analytics."""

from datetime import datetime, timezone
import logging

from sage.config import get_app_config
from sage.domain.qa.models import Chunk
from sage.integrations.bigquery.client import get_bigquery_client

log = logging.getLogger(__name__)


def log_question(question: str, chunks: list[Chunk], latency_ms: int) -> None:
    try:
        config = get_app_config()
        client = get_bigquery_client()
        table_id = f"{config.project_id}.{config.bq_dataset}.{config.bq_table}"
        row = {
            "asked_at": datetime.now(timezone.utc).isoformat(),
            "question": question,
            "sources": [c.source for c in chunks],
            "num_chunks": len(chunks),
            "latency_ms": latency_ms,
        }
        errors = client.insert_rows_json(table_id, [row])
        if errors:
            log.warning("Errori inserimento BigQuery: %s", errors)
    except Exception:
        log.warning("Scrittura BigQuery fallita (ignorata)", exc_info=True) 