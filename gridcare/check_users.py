from database import init_db

conn = init_db()
cur = conn.cursor()
cur.execute('SELECT user_id, username, role FROM users')
rows = cur.fetchall()

print("Users currently in the database:")
for row in rows:
    print(row)

conn.close()
