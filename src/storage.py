import sqlite3
from pathlib import Path

from src.request_workflow import Request, RequestStore, advance_id_counter

DEFAULT_PATH = "requests.db"
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema.sql"


def _connect(path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    return conn


def load_store(path=DEFAULT_PATH) -> RequestStore:
    store = RequestStore()
    try:
        conn = _connect(path)
        try:
            rows = conn.execute("SELECT * FROM requests ORDER BY id").fetchall()
        finally:
            conn.close()
    except sqlite3.DatabaseError as exc:
        raise ValueError(f"Cannot read data file {path}: {exc}") from exc

    for row in rows:
        store.add(Request.from_dict(dict(row)))
    highest = max((row["id"] for row in rows), default=0)
    advance_id_counter(highest)
    return store


def save_store(store: RequestStore, path=DEFAULT_PATH) -> None:
    conn = _connect(path)
    try:
        with conn:  # one transaction: commits on success, rolls back on error
            for r in store.list_all():
                conn.execute(
                    """
                    INSERT INTO requests (id, requester, amount, description, status, approver)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        requester   = excluded.requester,
                        amount      = excluded.amount,
                        description = excluded.description,
                        status      = excluded.status,
                        approver    = excluded.approver
                    """,
                    (r.id, r.requester, r.amount, r.description, r.status.value, r.approver),
                )
    finally:
        conn.close()