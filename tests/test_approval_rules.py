import pytest

from src.approval_rules import (
    DEPARTMENT_MANAGER,
    FINANCE_DIRECTOR,
    TEAM_LEAD,
    required_approver,
)


@pytest.mark.parametrize(
    "amount, expected",
    [
        (1, TEAM_LEAD),
        (499, TEAM_LEAD),
        (499.99, TEAM_LEAD),
        (500, DEPARTMENT_MANAGER),
        (2500, DEPARTMENT_MANAGER),
        (5000, DEPARTMENT_MANAGER),
        (5000.01, FINANCE_DIRECTOR),
        (5001, FINANCE_DIRECTOR),
        (1000000, FINANCE_DIRECTOR),
    ],
)
def test_required_approver(amount, expected):
    assert required_approver(amount) == expected


@pytest.mark.parametrize("amount", [0, -1, -500])
def test_non_positive_amounts_rejected(amount):
    with pytest.raises(ValueError):
        required_approver(amount)


@pytest.mark.parametrize("amount", ["500", None, True, [100]])
def test_non_numeric_amounts_rejected(amount):
    with pytest.raises(ValueError):
        required_approver(amount)