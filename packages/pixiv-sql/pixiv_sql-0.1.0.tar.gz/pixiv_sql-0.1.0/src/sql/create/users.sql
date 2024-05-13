CREATE TABLE
    IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name STRING,
        account STRING,
        is_followed INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );