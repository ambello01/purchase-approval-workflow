from src.request_workflow import Request, RequestStore, Status
from src.storage import load_store, save_store


def test_missing_file_gives_empty_store(tmp_path):
    store = load_store(tmp_path / "nope.json")
    assert store.list_all() == []


def test_round_trip_preserves_requests(tmp_path):
    path = tmp_path / "data.json"
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
    path = tmp_path / "data.json"
    store = RequestStore()
    first = store.add(Request(requester="ana", amount=10, description="Pens"))
    save_store(store, path)

    loaded = load_store(path)
    new = loaded.add(Request(requester="bo", amount=20, description="Paper"))
    assert new.id > first.id