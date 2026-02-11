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
    arquivos = glob.glob(f"raw/clima_openmeteo_{cidade}_*.json")
    
    if not arquivos:
        print(f"Nenhum arquivo encontrado para {cidade}")
        return None

    # 2. Pegamos o arquivo mais recente (o último da lista)
    arquivo_recente = max(arquivos, key=os.path.getctime)
    
    print(f"Lendo dados de: {arquivo_recente}")
    
    with open(arquivo_recente, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    return dados

def transform_to_dataframe(dados_json):

    #o JSON da Open_Meteo guarda os dados dentro da chave 'hourly'
    hourly_data = dados_json['hourly']

    #criamos o dataframe
    df = pd.DataFrame(hourly_data)

    #renomeando as colunas 
    df.rename(columns={
        'time': 'data_hora',
        'temperature_2m' : 'temperatura',
        'precipitation': 'chuva',
        'wind_speed_10m' : 'vento'
    }, inplace=True)

    #converte a coluna de data para o formato real
    df['data_hora'] = pd.to_datetime(df['data_hora'])

    # Extraindo inteligência da data
    df['mes'] = df['data_hora'].dt.month
    df['dia'] = df['data_hora'].dt.day
    df['hora'] = df['data_hora'].dt.hour

    return df

#BLOCO TESTE PARA VER O RESULTADO 

if __name__ == "__main__":
    cidade_teste = "Sao_Paulo"

    print(f"--- TESTANDO TRANSFORMAÇÃO PARA: {cidade_teste}---")

    dados_brutos = load_raw_data(cidade_teste)

    if dados_brutos:
        df_limpo = transform_to_dataframe(dados_brutos)

        print("\n Tabela criada com sucesso")
        print(df_limpo.head(10))

        print("\n Resumo estatístico dos dados: ")
        print(df_limpo.describe())

        print("\nTemperatura Média por Mês:")
        # agrupar por mês, pegar a temperatura e tirar a média
        print(df_limpo.groupby('mes')['temperatura'].mean())

def save_processed_data(df, cidade: str):
    """
    (LOAD)
    """
    os.makedirs('processed', exist_ok=True)
    
    clima_tempo = f"processed/clima_limpo_{cidade}.csv"

    df.to_csv(clima_tempo, index=False, encoding='utf-8')
    
    print(f"Guardado em: {clima_tempo}")

print("\nVerificando")
print(df_limpo.info())

print("\nNulos")
print(df_limpo.isna().sum())

if __name__ == "__main__":
    cidades = ["Sao_Paulo", "Belo_Horizonte", "Presidente_Prudente", "Sao_Jose_do_Rio_Preto"]
    
    print(f"Iniciando Processamento de {len(cidades)} cidades...\n")

    for cidade in cidades:
        print(f"--- Processando: {cidade} ---")
        
        dados_brutos = load_raw_data(cidade)
        
        if dados_brutos:
            df_limpo = transform_to_dataframe(dados_brutos)
            
            #Resultados
            save_processed_data(df_limpo, cidade)
            print(f" {cidade} finalizada com sucesso!\n")
        else:
            print(f" Pulando {cidade} por falta de dados.\n")

    print("PROCESSO TOTAL CONCLUÍDO!")