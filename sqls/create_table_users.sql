CREATE TABLE IF NOT EXISTS users (
    user_id integer PRIMARY KEY,
    user_name text NOT NULL,
    createdts timestamp NOT NULL
);
