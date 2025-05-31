INSERT_USER = """
    INSERT INTO users (email, password)
    VALUES (:email, :password)
    RETURNING id, email, password;
"""

FETCH_USER_BY_CREDENTIALS = """
    SELECT 
        u.id
        u.email
        u.is_active
    FROM users u
    WHERE
        u.email = :email
        AND u.password = :password
"""