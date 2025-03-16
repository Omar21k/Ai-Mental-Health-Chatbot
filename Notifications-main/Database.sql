import sqlite3 as sqCREATE 

CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    quote TEXT,
    scheduled_time DATETIME,
    status TEXT DEFAULT 'pending'
);
