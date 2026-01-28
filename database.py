import sqlite3
import os

DB_PATH = "game_data.db"


def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE achievements (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            unlocked BOOLEAN,
            progress INTEGER,
            max_progress INTEGER
        )''')
        c.execute("INSERT OR IGNORE INTO achievements VALUES (1, 'Первый прыжок', 'Соверши первый прыжок', 0, 0, 1)")
        c.execute("INSERT OR IGNORE INTO achievements VALUES (2, 'Сто шагов', 'Пройди 100 шагов', 0, 0, 100)")
        c.execute("INSERT OR IGNORE INTO achievements VALUES (3, 'Охотник на летучих мышей', 'Убей 50 врагов', 0, 0, 50)")
        conn.commit()
        conn.close()


def load_achievements():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM achievements")
    rows = c.fetchall()
    conn.close()
    return [
        {
            'id': r[0], 'name': r[1], 'description': r[2],
            'unlocked': bool(r[3]), 'progress': r[4], 'max_progress': r[5]
        }
        for r in rows
    ]


def reset_achievements():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE achievements SET progress = 0, unlocked = 0")
    conn.commit()
    conn.close()


def update_achievement(ach_id, progress=1):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE achievements SET progress = progress + ? WHERE id = ?", (progress, ach_id))
    c.execute("UPDATE achievements SET unlocked = 1 WHERE id = ? AND progress >= max_progress", (ach_id,))
    conn.commit()
    conn.close()
