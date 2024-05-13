CREATE TABLE
    IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY,
        title STRING,
        type STRING,
        caption STRING,
        user_id INTEGER,
        visible INTEGER,
        illust_ai_type INTEGER,
        illust_book_style INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );