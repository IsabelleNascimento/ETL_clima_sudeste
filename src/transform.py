import pandas as pd
import json
import os
import glob

def load_raw_data(cidade: str):
    """
    Função para encontrar o arquivo JSON mais recente de uma cidade
    na pasta 'raw' e carregá-lo.
    """
    # 1. Procuramos todos os arquivos que começam com o nome da cidade
    arquivos = glob.glob(f"raw/clima_historico_{cidade}_*.json")
    
    if not arquivos:
        print(f"⚠️ Nenhum arquivo encontrado para {cidade}")
        return None

    # 2. Pegamos o arquivo mais recente (o último da lista)
    arquivo_recente = max(arquivos, key=os.path.getctime)
    
    print(f"📖 Lendo dados de: {arquivo_recente}")
    
    with open(arquivo_recente, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    return dados
