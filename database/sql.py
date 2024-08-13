import sqlite3
import config

sql = sqlite3.connect(config.DB_path, check_same_thread=False)
db = sql.cursor()

db.execute('''CREATE TABLE IF NOT EXISTS server(
           id INTEGER PRIMARY KEY, 
           always TEXT,
           admin_mode TEXT,
           play_song TEXT
)''')
sql.commit()

def add_to_db(id: int, always: str, adminmode: str, playsong):
    db.execute("INSERT OR IGNORE INTO server (id, always, admin_mode, play_song) VALUES (?, ?, ?, ?)", (id, always, adminmode, playsong))
    sql.commit()

def select_from_db(id: int, obj: str):
    db.execute(f"SELECT {obj} FROM server WHERE id = ?", (id,))   
    value = db.fetchone()[0]

    if value is None:
        add_to_db(id, "off", "off", None)
        sql.commit()

        db.execute(f"SELECT {obj} FROM server WHERE id = ?", (id,))   
        value = db.fetchone()[0]

    return value

def update_in_db(id: int, obj: str, value: str):
    db.execute(f"UPDATE server SET {obj} = ? WHERE id = ?", (value, id))
    sql.commit()  