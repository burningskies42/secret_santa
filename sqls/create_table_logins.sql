CREATE TABLE IF NOT EXISTS logins (
    ip_address text,
    login text NOT NULL,
    createdts timestamp NOT NULL
);
