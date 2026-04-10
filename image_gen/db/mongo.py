from __future__ import annotations

import os
from typing import Any, Optional

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from image_gen.core.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

_client: Optional[MongoClient] = None
_db: Optional[Any] = None


def get_db() -> Optional[Any]:
    global _client, _db
    if _db is not None:
        return _db

    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        return None

    try:
        _client = MongoClient(
            mongo_uri,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=1000,
            connectTimeoutMS=1000,
            socketTimeoutMS=1000,
        )
        _client.admin.command("ping")
        _db = _client[os.getenv("MONGO_DB_NAME", "comic_ai")]
        return _db
    except PyMongoError as exc:
        logger.warning("Unable to access AiToon DB: %s", exc)
        _client = None
        _db = None
        return None
