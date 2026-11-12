from dataclasses import dataclass
from enum import Enum
from itertools import count

# ADJUST THIS IMPORT to match your threshold module and function name
from src.approval_rules import required_approver as get_approver


class Status(Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class InvalidTransition(Exception):
    """Raised when an action is not allowed in the request's current status."""


_id_counter = count(1)


@dataclass
class Request:
    requester: str
    amount: float
    description: str
    id: int = 0
    status: Status = Status.DRAFT
    approver: str | None = None

    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero")
        if not self.id:
            self.id = next(_id_counter)

    def submit(self):
        if self.status is not Status.DRAFT:
            raise InvalidTransition(f"Cannot submit a request in status {self.status.value}")
        self.approver = get_approver(self.amount)
        self.status = Status.SUBMITTED

    def approve(self):
        if self.status is not Status.SUBMITTED:
            raise InvalidTransition(f"Cannot approve a request in status {self.status.value}")
        self.status = Status.APPROVED

    def reject(self):
        if self.status is not Status.SUBMITTED:
            raise InvalidTransition(f"Cannot reject a request in status {self.status.value}")
        self.status = Status.REJECTED


class RequestStore:
    """In-memory storage for requests."""

    def __init__(self):
        self._requests: dict[int, Request] = {}

    def add(self, request: Request) -> Request:
        self._requests[request.id] = request
        return request

    def get(self, request_id: int) -> Request:
        try:
            return self._requests[request_id]
        except KeyError:
            raise KeyError(f"No request with id {request_id}")

    def list_by_status(self, status: Status) -> list[Request]:
        return [r for r in self._requests.values() if r.status is status]