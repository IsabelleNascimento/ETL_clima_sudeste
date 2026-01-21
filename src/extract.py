import requests
import json
from datetime import datetime
import time
import os

CIDADES_SUDESTE = {
    "Presidente_Prudente": {"lat": -22.12, "lon": -51.38},
    "Sao_Paulo": {"lat": -23.55, "lon": -46.63},
    "Sao_Jose_do_Rio_Preto": {"lat": -20.81, "lon": -49.38},
    "Belo_Horizonte": {"lat": -19.91, "lon": -43.93} 
}

def extract_openmeteo_data(cidades: dict):

    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    base_params = {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "timezone": "America/Sao_Paulo"
    }

    os.makedirs('raw', exist_ok=True) 

    print("--- INICIANDO EXTRAÇÃO OPEN-METEO (DADOS HISTÓRICOS) ---")

    for nome_cidade, coords in cidades.items():
        print(f"\nColetando dados para: {nome_cidade}...")
        params = base_params.copy()
        params["latitude"] = coords["lat"]
        params["longitude"] = coords["lon"]
        
        try:
            # Fazendo a requisição
            response = requests.get(BASE_URL, params=params, timeout=15)
            
            # Tratamento de Erros
            response.raise_for_status() 

            # Convertendo para JSON
            data = response.json()
            
            # Salvando o Arquivo Bruto 
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"raw/clima_openmeteo_{nome_cidade}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"✅ Sucesso! Dados brutos salvos em {filename}")

        except requests.exceptions.HTTPError as err:
            print(f"❌ Erro HTTP ao coletar {nome_cidade}: {err}. Revise a URL/Parâmetros.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conexão ao coletar {nome_cidade}: {e}. Verifique sua internet.")
        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado: {e}")
            
        time.sleep(1) 


# PONTO DE ENTRADA
if __name__ == "__main__":
    extract_openmeteo_data(CIDADES_SUDESTE)