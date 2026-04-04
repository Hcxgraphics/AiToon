import json
from pathlib import Path

from jsonschema import ValidationError, validate


SCHEMA_PATH = Path(__file__).resolve().with_name("master_schema.json")


def load_master_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_master(output, schema=None):
    try:
        validate(instance=output, schema=schema or load_master_schema())
        return True, None
    except ValidationError as exc:
        return False, str(exc)
