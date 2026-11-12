import pytest

from src.request_workflow import InvalidTransition, Request, RequestStore, Status


def make_request(amount=100):
    return Request(requester="alice", amount=amount, description="Test purchase")


def test_new_request_starts_as_draft():
    r = make_request()
    assert r.status is Status.DRAFT
    assert r.approver is None


def test_ids_are_unique():
    assert make_request().id != make_request().id


def test_non_positive_amount_rejected():
    with pytest.raises(ValueError):
        make_request(amount=0)
    with pytest.raises(ValueError):
        make_request(amount=-5)


def test_submit_moves_to_submitted_and_assigns_approver():
    r = make_request()
    r.submit()
    assert r.status is Status.SUBMITTED
    assert r.approver is not None


def test_submit_twice_fails():
    r = make_request()
    r.submit()
    with pytest.raises(InvalidTransition):
        r.submit()


def test_approve_after_submit():
    r = make_request()
    r.submit()
    r.approve()
    assert r.status is Status.APPROVED


def test_reject_after_submit():
    r = make_request()
    r.submit()
    r.reject()
    assert r.status is Status.REJECTED


def test_cannot_approve_draft():
    with pytest.raises(InvalidTransition):
        make_request().approve()


def test_cannot_reject_draft():
    with pytest.raises(InvalidTransition):
        make_request().reject()


def test_cannot_change_decision_once_made():
    r = make_request()
    r.submit()
    r.approve()
    with pytest.raises(InvalidTransition):
        r.reject()


def test_store_add_and_get():
    store = RequestStore()
    r = store.add(make_request())
    assert store.get(r.id) is r


def test_store_get_missing_raises():
    with pytest.raises(KeyError):
        RequestStore().get(999)


def test_store_list_by_status():
    store = RequestStore()
    a = store.add(make_request())
    b = store.add(make_request())
    a.submit()
    assert store.list_by_status(Status.SUBMITTED) == [a]
    assert store.list_by_status(Status.DRAFT) == [b]