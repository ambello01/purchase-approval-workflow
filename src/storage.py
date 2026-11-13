import json
from pathlib import Path

from src.request_workflow import Request, RequestStore, advance_id_counter

DEFAULT_PATH = "requests.json"


def load_store(path=DEFAULT_PATH) -> RequestStore:
    store = RequestStore()
    p = Path(path)
    if not p.exists():
        return store
    data = json.loads(p.read_text(encoding="utf-8"))
    highest = 0
    for item in data:
        request = Request.from_dict(item)
        store.add(request)
        highest = max(highest, request.id)
    advance_id_counter(highest)
    return store


def save_store(store: RequestStore, path=DEFAULT_PATH) -> None:
    data = [r.to_dict() for r in store.list_all()]
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")

def load_store(path=DEFAULT_PATH) -> RequestStore:
    store = RequestStore()
    p = Path(path)
    if not p.exists():
        advance_id_counter(0)          # <-- NEW: reset to start at 1
        return store

    data = json.loads(p.read_text())
    for item in data:
        store.add(Request.from_dict(item))
    highest = max((item["id"] for item in data), default=0)
    advance_id_counter(highest)        # <-- make sure this runs even when data is empty
    return store
