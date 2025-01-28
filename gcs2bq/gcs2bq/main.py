from google.cloud import storage
from google.cloud import bigquery
import pandas as pd
from io import BytesIO

# Função para carregar todos os arquivos Excel do bucket e ler a aba específica 'Relatório Mês.Anterior'
def load_all_excel_from_folder(bucket_name, bucket_folder, sheet_name):
    storage_client = storage.Client()  # Cliente para interagir com o Google Cloud Storage
    folder_path_bucket = f"{bucket_folder}/"  # Adiciona a barra ao caminho da pasta do bucket
    blobs = storage_client.list_blobs(bucket_name, prefix=folder_path_bucket)

    dataframes = []  # Lista para armazenar os dataframes lidos

    for blob in blobs:
        # Verifica se o arquivo é Excel
        if blob.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            print(f"Lendo arquivo: {blob.name}")
            content = blob.download_as_bytes()
            df = pd.read_excel(BytesIO(content), sheet_name=sheet_name)
            dataframes.append(df)  # Adiciona o dataframe à lista

    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()


# Função para verificar se a tabela existe e criar se não existir
def ensure_table_exists(dataframe, dataset_id, table_id):
    bigquery_client = bigquery.Client()
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)

    try:
        bigquery_client.get_table(table_ref)
        print(f"Tabela `{table_id}` já existe.")
    except NotFound:
        schema = []
        for name, dtype in zip(dataframe.columns, dataframe.dtypes):
            field_type = "STRING" if dtype == 'object' else "FLOAT" if dtype == 'float64' else "INTEGER" if dtype == 'int64' else "STRING"
            schema.append(bigquery.SchemaField(name, field_type))
        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)
        print(f"Tabela `{table_id}` criada.")
    except Exception as e:
        print(f"Erro ao verificar/criar a tabela: {e}")


# Função para realizar o Merge no BigQuery
def upsert_to_bigquery(dataframe, dataset_id, table_id, unique_key_columns):
    bigquery_client = bigquery.Client()
    ensure_table_exists(dataframe, dataset_id, table_id)
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)
    query = f"SELECT {', '.join(unique_key_columns)} FROM `{dataset_id}.{table_id}`"
    existing_keys = bigquery_client.query(query).to_dataframe()
    merged_df = dataframe.merge(existing_keys, on=unique_key_columns, how='left', indicator=True)
    new_records = merged_df[merged_df['_merge'] == 'left_only'].drop(columns='_merge')
    if not new_records.empty:
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
        job = bigquery_client.load_table_from_dataframe(new_records, table_ref, job_config=job_config)
        job.result()
    else:
        print("Nenhum novo registro para adicionar.")


# Função principal que combina tudo
def process_data(bucket_name, bucket_folder, sheet_name, dataset_id, table_id, unique_key_columns):
    # Carrega os dados do GCS para um DataFrame
    dataframe = load_all_excel_from_folder(bucket_name, bucket_folder, sheet_name)

    if not dataframe.empty:
        # Realiza o upsert para o BigQuery
        upsert_to_bigquery(dataframe, dataset_id, table_id, unique_key_columns)
        print("Dados carregados e atualizados com sucesso.")
    else:
        print("Nenhum dado encontrado para carregar.")

# Executando a função principal
if __name__ == "__main__":
    print("Este script não deve ser executado diretamente. Use o script 'run_processing.py' para chamar a função process_data.")



import gcs2bq

# Defina suas variáveis de configuração
project_id = "elet-dados-compulsorio-dev"
bucket_name = "cs_elet_compulsorio_raw_analise_provisao_dev"
bucket_folder = "teste"
sheet_name = "Relatório Mês.Anterior"
dataset_id = "ds_elet_compulsorio_refined_analise_provisao"
table_id = "valid"
unique_key_columns = ["DOSSIE"]