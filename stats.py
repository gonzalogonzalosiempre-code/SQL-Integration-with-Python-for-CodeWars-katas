import sqlite3


conn = sqlite3.connect('katas.db')
curr = conn.cursor()
curr.execute("SELECT SUBSTR(completedAt,1,7) AS mes, COUNT(*) AS total_katas FROM kata GROUP BY mes")
result = curr.fetchall()
for fila in result:
    print(fila)