"""Reads additional system instructions from Cloud Storage on every request."""

from functools import lru_cache
import logging

from google.cloud import storage

from sage.config import get_app_config

log = logging.getLogger(__name__)


@lru_cache
def get_storage_client() -> storage.Client:
    config = get_app_config()
    return storage.Client(project=config.project_id)


def load_instructions() -> str:
    """Download `istruzioni.md` from `<prefix>-instructions` bucket at request time."""
    config = get_app_config()
    if not config.instructions_bucket:
        return ""
    try:
        client = get_storage_client()
        bucket = client.bucket(config.instructions_bucket)
        blob = bucket.blob(config.instructions_blob)
        return blob.download_as_text(encoding="utf-8").strip()
    except Exception:
        log.warning(
            "Impossibile leggere gs://%s/%s: procedo senza istruzioni aggiuntive",
            config.instructions_bucket,
            config.instructions_blob,
            exc_info=True,
        )
        return ""
    