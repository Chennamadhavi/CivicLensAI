import sqlite3

conn = sqlite3.connect("complaints.db")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(complaints)")

rows = cursor.fetchall()

print("Columns:")

for row in rows:
    print(row)

conn.close()