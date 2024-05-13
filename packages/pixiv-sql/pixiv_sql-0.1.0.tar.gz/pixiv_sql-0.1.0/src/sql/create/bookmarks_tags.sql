CREATE TABLE
    IF NOT EXISTS bookmarks_tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bookmark_id INTEGER,
        tag_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (bookmark_id) REFERENCES bookmarks (id),
        FOREIGN KEY (tag_id) REFERENCES tags (id)
    );