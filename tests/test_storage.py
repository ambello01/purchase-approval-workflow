import pytest

from src.request_workflow import Request, RequestStore, Status
from src.storage import load_store, save_store


def test_missing_file_gives_empty_store(tmp_path):
    store = load_store(tmp_path / "nope.db")
    assert store.list_all() == []


def test_round_trip_preserves_requests(tmp_path):
    path = tmp_path / "data.db"
    store = RequestStore()
    r = store.add(Request(requester="ana", amount=750, description="Monitors"))
    r.submit()
    save_store(store, path)

    loaded = load_store(path)
    again = loaded.get(r.id)
    assert again.status is Status.SUBMITTED
    assert again.approver == "Department manager"
    assert again.amount == 750


def test_new_ids_do_not_collide_after_load(tmp_path):
    path = tmp_path / "data.db"
    store = RequestStore()
    first = store.add(Request(requester="ana", amount=10, description="Pens"))
    save_store(store, path)

    loaded = load_store(path)
    new = loaded.add(Request(requester="bo", amount=20, description="Paper"))
    assert new.id > first.id


def test_corrupt_file_raises_value_error(tmp_path):
    path = tmp_path / "data.db"
    path.write_text("this is not a sqlite database, just text padding " * 10)
    with pytest.raises(ValueError):
        load_store(path)


def test_update_persists_status_change(tmp_path):
    path = tmp_path / "data.db"
    store = RequestStore()
    r = store.add(Request(requester="ana", amount=750, description="Monitors"))
    save_store(store, path)

    r.submit()
    r.approve()
    save_store(store, path)  # second save must update, not duplicate

    loaded = load_store(path)
    assert len(loaded.list_all()) == 1
    assert loaded.get(r.id).status is Status.APPROVED