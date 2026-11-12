"""Threshold rules for routing purchase requests to the right approver."""

TEAM_LEAD = "Team lead"
DEPARTMENT_MANAGER = "Department manager"
FINANCE_DIRECTOR = "Finance director"

# Upper limits are inclusive: 5,000 goes to the department manager.
TEAM_LEAD_LIMIT = 500        # amounts below this go to the team lead
MANAGER_LIMIT = 5000         # amounts up to and including this go to the manager


def required_approver(amount):
    """Return the approver required for a purchase amount.

    Raises ValueError if the amount is not a positive number.
    """
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if amount < TEAM_LEAD_LIMIT:
        return TEAM_LEAD
    if amount <= MANAGER_LIMIT:
        return DEPARTMENT_MANAGER
    return FINANCE_DIRECTOR