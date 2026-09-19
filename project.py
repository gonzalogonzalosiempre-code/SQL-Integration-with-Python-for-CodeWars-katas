import requests
import json
import time

def main():
    resk = []
    r = requests.get("https://www.codewars.com/api/v1/users/gonzalogonzalosiempre-code/code-challenges/completed?page=https://www.codewars.com/users/gonzalogonzalosiempre-code/completed_solutions")
    datos = r.json()
    for kata in datos['data']:
        tmp = {"name" : kata['name'], "id" : kata['id'],"rank.name": "", "completedLanguages" : " ".join(kata['completedLanguages']), "completedAt" : kata['completedAt']}
        k = requests.get(f"https://www.codewars.com/api/v1/code-challenges/{kata['id']}")
        detalle = k.json()
        kyu = detalle['rank']['name']
        tmp["rank.name"] = kyu
        resk.append(tmp)
        time.sleep(1)
    with open('Datos.json', 'w') as file:
        json.dump(resk, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()