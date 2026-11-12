# Purchase Request Approval Workflow

A prototype that routes purchase requests to the right approver based on the request amount.

## What it does
- Employees submit a purchase request with an amount and description
- The system applies threshold rules to decide who must approve it
- Approvers can approve or reject, and the status is tracked

## Approval rules
| Purchase amount | Approver required |
|-----------------|-------------------|
| Under 500       | Team lead         |
| 500 to 5,000    | Department manager|
| Over 5,000      | Finance director  |

See [docs/approval-thresholds.md](docs/approval-thresholds.md) for details and [docs/user-stories.md](docs/user-stories.md) for requirements.

## Project status
Early prototype. Documentation is in place; code is coming.

## How to run
Instructions will be added once the code is written.

## Author
Modibbo AHMADOU BELLO