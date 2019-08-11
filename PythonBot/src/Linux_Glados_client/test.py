import sqlite3
import os
import sys

conn = sqlite3.connect(os.path.join(sys.path[0],"assets/playlist_database.db"))
c = conn.cursor()
sql = "SELECT * FROM my_playlist"
print(c.execute(sql))
conn.close()