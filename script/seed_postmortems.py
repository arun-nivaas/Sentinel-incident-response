import json
from pathlib import Path
from dotenv import load_dotenv
from app.database.database import SessionLocal
from app.models.postmortem import Postmortem
from app.service.embedding_service import EmbeddingService
from typing import Dict,Any

load_dotenv()

DATA_FILE = Path(__file__).resolve().parents[1] /"postmortems.json"


def load_postmortems() -> list[Dict[str,Any]]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def seed():
    db = SessionLocal()
    embedding_service = EmbeddingService()

    try:
        existing_count = db.query(Postmortem).count()
        if existing_count > 0:
            print(f"Postmortems table already has {existing_count} rows. Skipping seed.")
            return

        postmortems = load_postmortems()

        for pm in postmortems:
            vector = embedding_service.embed_text(pm["summary"])
            record = Postmortem(
                service_name=pm["service_name"],
                error_type=pm["error_type"],
                summary=pm["summary"],
                embedding=vector,
            )
            db.add(record)
            print(f"Seeded: {pm['service_name']} — {pm['error_type']}")

        db.commit()
        print(f"\nSeeded {len(postmortems)} postmortems successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()