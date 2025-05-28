INSERT_USER = """
    INSERT INTO users (email, password)
    VALUES (:email, :password)
    RETURNING id, email, password;
"""