import sqlite3
import json

def extract():
    ##1. Empezando...
    with open("Datos.json", 'r') as file:
        datos = json.load(file)
    ##2. Datos leídos, cantidad: {len(datos)}
    connect = sqlite3.connect('katas.db')
    ##3. Conectado a la base de datos
    cursor = connect.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kata(
    id VARCHAR(50),
    name VARCHAR(50) UNIQUE,
    rank_name VARCHAR(15),
    completedLanguages VARCHAR(10),
    completedAt DATE,
    PRIMARY KEY(id)
    );""")
    ##4. Tabla creada (o ya existía)
    tmp = [(d["id"],d["name"],d["rank.name"],d["completedLanguages"],d["completedAt"]) for d in datos]
    ##5. Tuplas preparadas: {len(tmp)}      
    cursor.executemany("""
    INSERT OR IGNORE INTO kata(id,name,rank_name,completedLanguages,completedAt)
    VALUES(?,?,?,?,?);""",tmp)
    ##6. Insert ejecutado
    connect.commit()
    ##7. Commit hecho
    connect.close()
    ##8. Conexión cerrada, TERMINADO"
if __name__ == '__main__':
    extract()