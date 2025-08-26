from datetime import datetime, timezone
from tools.firestore_writer import get_db, upsert_artist, add_dataset_row

def main():
    db = get_db()

    style_id = "writer_test"
    ok = upsert_artist(db, style_id, {
        "style_id": style_id,
        "name": "Smoke Test Artist",
        "updated_at": datetime.now(timezone.utc).isoformat()
    })
    print("Artist write:", ok)

    row_id = add_dataset_row(db, {
        "song_id": f"test_{int(datetime.now(timezone.utc).timestamp())}",
        "artist_placeholder": "Smoke Test Artist",
        "title": "Cloud Smoke",
        "themes": '["test","firestore"]',
        "structure": "Verse-Chorus",
        "notes_annotations": "Inserted by test script"
    })
    print("Dataset write:", row_id)

if __name__ == "__main__":
    main()
