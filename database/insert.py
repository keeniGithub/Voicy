import sqlite3
import config

sql = sqlite3.connect(config.DB_path,  check_same_thread=False)
db = sql.cursor()

db.execute('''CREATE TABLE IF NOT EXISTS server
             (id INTEGER PRIMARY KEY, always TEXT)''')
sql.commit()

print("Success!")