import pytest

from src.cli import main


@pytest.fixture
def data_file(tmp_path):
    return str(tmp_path / "requests.json")


def run(data_file, *args):
    return main(["--file", data_file, *args])


def create_one(data_file, amount="750"):
    return run(
        data_file, "create", "--requester", "ana",
        "--amount", amount, "--description", "Monitors",
    )


def test_create_and_show(data_file, capsys):
    assert create_one(data_file) == 0
    capsys.readouterr()
    assert run(data_file, "show", "1") in (0,)
    out = capsys.readouterr().out
    assert "DRAFT" in out and "ana" in out


def test_submit_routes_to_correct_approver(data_file, capsys):
    create_one(data_file, amount="6000")
    run(data_file, "submit", "1")
    out = capsys.readouterr().out
    assert "Finance director" in out


def test_full_approval_flow(data_file, capsys):
    create_one(data_file)
    run(data_file, "submit", "1")
    assert run(data_file, "approve", "1") == 0
    assert "APPROVED" in capsys.readouterr().out


def test_approve_draft_fails(data_file, capsys):
    create_one(data_file)
    capsys.readouterr()
    assert run(data_file, "approve", "1") == 1
    assert "Cannot approve" in capsys.readouterr().err


def test_unknown_id_fails(data_file, capsys):
    assert run(data_file, "show", "99") == 1
    assert "No request with id 99" in capsys.readouterr().err


def test_non_positive_amount_fails(data_file, capsys):
    assert create_one(data_file, amount="0") == 1
    assert "greater than zero" in capsys.readouterr().err


def test_list_filters_by_status(data_file, capsys):
    create_one(data_file)
    create_one(data_file)
    run(data_file, "submit", "1")
    capsys.readouterr()
    run(data_file, "list", "--status", "submitted")
    out = capsys.readouterr().out
    assert "#1" in out and "#2" not in out