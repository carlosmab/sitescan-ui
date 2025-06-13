INSERT_USER = """
    INSERT INTO users (email, password)
    VALUES (:email, :password)
    RETURNING id, email, password;
"""

FETCH_USER_BY_EMAIL = """
    SELECT 
        u.id
        u.email
        u.is_active
        u.password
    FROM users u
    WHERE
        u.email = :email
"""