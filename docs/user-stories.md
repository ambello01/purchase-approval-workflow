# User Stories and Acceptance Criteria

## Story 1: Submit a purchase request
As a requester, I want to submit a purchase request with an amount and
a cost centre, so that it enters the approval process.

**Acceptance criteria**
- A request must have a positive amount.
- A request starts with the status "Pending approval".

## Story 2: Approval routing by threshold
As a finance manager, I want requests routed to approvers based on
amount, so that spending follows our delegation of authority.

**Acceptance criteria**
- Requests up to 1,000 need one approval (budget holder).
- Requests up to 10,000 need two approvals (budget holder, finance manager).
- Requests above 10,000 need three approvals (budget holder, finance manager, CFO).

## Story 3: Separation of duties
As an auditor, I want to make sure nobody approves their own request,
so that the control is effective.

**Acceptance criteria**
- A requester cannot approve their own request.