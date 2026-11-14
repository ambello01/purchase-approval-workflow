CREATE TABLE IF NOT EXISTS requests (
    id          INTEGER PRIMARY KEY,
    requester   TEXT    NOT NULL,
    amount      REAL    NOT NULL CHECK (amount > 0),
    description TEXT    NOT NULL,
    status      TEXT    NOT NULL,
    approver    TEXT
);