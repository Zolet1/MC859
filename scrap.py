import pandas as pd
import requests
import json
import time

# Ler o arquivo CSV contendo os IDs dos jogadores
players = pd.read_csv("data/players.csv")

base_url = "https://www.transfermarkt.com.br/ceapi/marketValueDevelopment/graph/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}

# Lista para armazenar os dados extraídos
data_extracted = []
cont = 0
total = str(len(players))
for player_id in players["player_id"]:
    cont = cont + 1
    data_url = f"{base_url}{player_id}"
    response = requests.get(data_url, headers=headers)
    
    if response.status_code == 200:
        json_data = response.json()  # Converte a resposta em JSON para um dicionário Python
        
        # Percorre cada item da lista "list" no JSON
        for item in json_data["list"]:
            data_extracted.append({
                "player_id": player_id,
                "value": item.get("mw", ""),
                "date": item.get("datum_mw", ""),
                "club_name": item.get("verein", ""),
                "age": item.get("age", "")
            })
    else:
        print(f"Failed with status code: {response.status_code} for URL: {data_url}")

    print("ID: "+str(player_id)+" Progresso: "+str(cont)+ "/" + total)
    time.sleep(1)  # Opcional: Evitar rate limiting

# Converte a lista de dados extraídos em um DataFrame
df = pd.DataFrame(data_extracted)

# Salva o DataFrame em um arquivo CSV
df.to_csv("players_values.csv", index=False)

print("Dados extraídos e salvos em 'players_values.csv'.")