INSERT_SCAN = """
    INSERT INTO scans (user_id, url)
    VALUES (:user_id, :url)
    RETURNING 
        id, 
        user_id, 
        created_at, 
        url, 
        scrapped_at, 
        scrap_result_json,
        analysed_at,
        analysis_result_json
    ;
"""

FETCH_SCANS_BY_USER_ID = """
    SELECT 
        id, 
        user_id, 
        created_at, 
        url, 
        scrapped_at, 
        scrap_result_json,
        analyzed_at,
        analysis_result_json
    FROM 
        scans
    WHERE
        user_id = :user_id
"""

FETCH_SCANS_BY_ID = """
    SELECT 
        id, 
        user_id, 
        created_at, 
        url, 
        scrapped_at, 
        scrap_result_json,
        analyzed_at,
        analysis_result_json
    FROM 
        scans
    WHERE
        id = :id
"""


UPDATE_SCRAP_RESULT = """
    UPDATE
        scans
    SET
        scrapped_at = TIMESTAMP.NOW
        scrap_result = :scrap_result_json
    WHERE
        user_id = :user_id
"""


UPDATE_ANALYSIS_RESULT = """
    UPDATE
        scans
    SET
        analyzed_at = TIMESTAMP.NOW
        analysis_result = :analysis_result_json
    WHERE
        user_id = :user_id
"""