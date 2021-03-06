CREATE TABLE IF NOT EXISTS users (
    USER_ID integer PRIMARY KEY,
    USER_NAME text NOT NULL,
    USER_LOGIN text NOT NULL,
    USER_PASSWORD_HASH text NOT NULL,
    CREATEDTS timestamp NOT NULL,
    IS_ADMIN Boolean NOT NULL,
    COOKIE text,
    COOKIE_VALID_TO timestamp
);
