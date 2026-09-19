import requests
import json
import time
import sqlite3

def main():
    resk = get_datos()
    #Inicialize Sql
    namedb = 'katas.db'
    if sql_save(resk):
        stats_request(namedb)

def get_datos():
    Res = []
    r = requests.get("https://www.codewars.com/api/v1/users/gonzalogonzalosiempre-code/code-challenges/completed?page=https://www.codewars.com/users/gonzalogonzalosiempre-code/completed_solutions")
    datos = r.json()
    for kata in datos['data']:
        k = requests.get(f"https://www.codewars.com/api/v1/code-challenges/{kata['id']}")
        detalle = k.json()
        tmp = combined_datos(kata,detalle)
        Res.append(tmp)
        time.sleep(1)
    name = 'Datos.json'
    with open(name, 'w') as file:
        json.dump(Res, file, indent=4, ensure_ascii=False)
    return name

def combined_datos(kata,detalle):
    return {
        "name" : kata['name'], 
        "id" : kata['id'],
        "rank.name": detalle['rank']['name'],
        "completedLanguages" : format_datos(kata['completedLanguages']),
        "completedAt" : kata['completedAt']
        }
def format_datos(datos):
    return " ".join(datos)

def sql_save(Datos):
    ##1. Empezando...
    with open(Datos, 'r') as file:
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
    return True

def stats_request(database):
    conn = sqlite3.connect(database)
    curr = conn.cursor()
    conn.create_function("extract",1, extract_year_month)
    curr.execute("SELECT extract(completedAt) AS mes, COUNT(*) AS total_katas FROM kata GROUP BY mes")
    result = curr.fetchall()
    for fila in result:
        print(fila)
def extract_year_month(date):
    return date[:7]

if __name__ == '__main__':
    main()
