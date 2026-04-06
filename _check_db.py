import sqlite3
conn=sqlite3.connect(r'c:\Users\Jake\Documents\Coding Fun\practice\practice.db')
cur=conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cur.fetchall())
conn.close()
