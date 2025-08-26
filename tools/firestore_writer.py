import os
from typing import Dict, Any
from google.cloud import firestore

def get_db(creds_path: str = "service-account.json") -> firestore.Client:
    """
    Use a service account JSON (NOT committed to git).
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
    return firestore.Client()

def upsert_artist(db: firestore.Client, style_id: str, payload: Dict[str, Any]) -> None:
    db.collection("artists").document(style_id).set(payload, merge=True)

def add_dataset_row(db: firestore.Client, row: Dict[str, Any]) -> None:
    doc_id = row.get("song_id")
    if doc_id:
        db.collection("datasets").document(doc_id).set(row)
    else:
        db.collection("datasets").add(row)
from typing import Optional, Dict, Any
import logging

from google.cloud import firestore
from google.api_core import exceptions as gcloud_exceptions

logger = logging.getLogger(__name__)


def get_db(project: Optional[str] = None) -> firestore.Client:
    """Return a Firestore client using ADC or an explicit project.

    Raises the original exception on failure.
    """
    try:
        return firestore.Client(project=project) if project else firestore.Client()
    except Exception:
        logger.exception("Failed to create Firestore client")
        raise


def upsert_artist(db: firestore.Client, style_id: str, payload: Dict[str, Any]) -> bool:
    """Create or update an artist document.

    Returns True on success, False on error.
    """
    if not style_id:
        logger.error("style_id is required for upsert_artist")
        return False
    if not isinstance(payload, dict):
        logger.error("payload must be a dict")
        return False

    try:
        db.collection("artists").document(style_id).set(payload, merge=True)
        return True
    except (gcloud_exceptions.GoogleAPICallError, gcloud_exceptions.RetryError, Exception):
        logger.exception("Failed to upsert artist %s", style_id)
        return False


def add_dataset_row(db: firestore.Client, row: Dict[str, Any]) -> Optional[str]:
    """Add a dataset row. If row contains 'song_id', use it as the document ID.

    Returns the document ID on success, or None on failure.
    """
    if not isinstance(row, dict):
        logger.error("row must be a dict")
        return None

    try:
        doc_id = row.get("song_id")
        if doc_id:
            db.collection("datasets").document(doc_id).set(row)
            return str(doc_id)
        else:
            doc_ref, _ = db.collection("datasets").add(row)
            # DocumentReference.id is the generated ID
            return getattr(doc_ref, "id", None)
    except (gcloud_exceptions.GoogleAPICallError, gcloud_exceptions.RetryError, Exception):
        logger.exception("Failed to add dataset row")
        return None
    from datetime import datetime
from tools.firestore_writer import get_db, upsert_artist, add_dataset_row

def main():
    db = get_db()

    style_id = "writer_test"
    ok = upsert_artist(db, style_id, {
        "style_id": style_id,
        "name": "Smoke Test Artist",
        "updated_at": datetime.utcnow().isoformat()
    })
    print("Artist write:", ok)

    row_id = add_dataset_row(db, {
        "song_id": f"test_{int(datetime.utcnow().timestamp())}",
        "artist_placeholder": "Smoke Test Artist",
        "title": "Cloud Smoke",
        "themes": '["test", "firestore"]',
        "structure": "Verse-Chorus",
        "notes_annotations": "Inserted by test script"
    })
    print("Dataset write:", row_id)

if __name__ == "__main__":
    main()

