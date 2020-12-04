CREATE TABLE IF NOT EXISTS addresses (
    user_id integer PRIMARY KEY,
    user_address text NOT NULL,
    createdts timestamp NOT NULL
);
