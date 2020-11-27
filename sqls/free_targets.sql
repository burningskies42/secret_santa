SELECT
    u.USER_ID
    ,u.USER_NAME
    ,a.USER_ADDRESS
FROM
    USERS as u
INNER JOIN
    ADDRESSES as a
    ON u.USER_ID = a.USER_ID
LEFT JOIN
    SANTAS as s
    ON u.USER_ID = s.TARGET_ID
WHERE
    s.TARGET_ID is NULL
