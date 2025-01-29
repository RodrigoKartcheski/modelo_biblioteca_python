from google.cloud import storage
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import pandas as pd
from io import BytesIO


class LoadXlsxToBigQuery:
    def __init__(self, bucket_name, bucket_folder, sheet_name, dataset_id, table_id, unique_key_columns):
        self.bucket_name = bucket_name
        self.bucket_folder = bucket_folder
        self.sheet_name = sheet_name
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.unique_key_columns = unique_key_columns
        self.storage_client = storage.Client()
        self.bigquery_client = bigquery.Client()

    def load_all_excel_from_folder(self):
        folder_path_bucket = f"{self.bucket_folder}/"
        blobs = self.storage_client.list_blobs(self.bucket_name, prefix=folder_path_bucket)

        dataframes = []

        for blob in blobs:
            try:
                if blob.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    print(f"Lendo arquivo: {blob.name}")  # Usando print para mostrar o progresso
                    content = blob.download_as_bytes()
                    df = pd.read_excel(BytesIO(content), sheet_name=self.sheet_name)
                    dataframes.append(df)
            except Exception as e:
                print(f"Erro ao processar o arquivo {blob.name}: {e}")  # Usando print para erros

        return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

    def ensure_table_exists(self, dataframe):
        table_ref = self.bigquery_client.dataset(self.dataset_id).table(self.table_id)

        try:
            self.bigquery_client.get_table(table_ref)
            print(f"Tabela `{self.table_id}` já existe.")
        except NotFound:
            schema = []
            for name, dtype in zip(dataframe.columns, dataframe.dtypes):
                field_type = (
                    "STRING" if dtype == 'object'
                    else "FLOAT" if dtype == 'float64'
                    else "INTEGER" if dtype == 'int64'
                    else "STRING"
                )
                schema.append(bigquery.SchemaField(name, field_type))

            table = bigquery.Table(table_ref, schema=schema)
            self.bigquery_client.create_table(table)
            print(f"Tabela `{self.table_id}` criada.")
        except Exception as e:
            print(f"Erro ao verificar/criar a tabela `{self.table_id}`: {e}")

    def upsert_to_bigquery(self, dataframe):
        self.ensure_table_exists(dataframe)
        table_ref = self.bigquery_client.dataset(self.dataset_id).table(self.table_id)

        try:
            query = f"SELECT {', '.join(self.unique_key_columns)} FROM `{self.dataset_id}.{self.table_id}`"
            existing_keys = self.bigquery_client.query(query).to_dataframe()

            merged_df = dataframe.merge(existing_keys, on=self.unique_key_columns, how='left', indicator=True)
            new_records = merged_df[merged_df['_merge'] == 'left_only'].drop(columns='_merge')

            if not new_records.empty:
                job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
                job = self.bigquery_client.load_table_from_dataframe(new_records, table_ref, job_config=job_config)
                job.result()
                print(f"{len(new_records)} novos registros inseridos.")
            else:
                print("Nenhum novo registro para adicionar.")
        except Exception as e:
            print(f"Erro ao realizar o upsert na tabela `{self.table_id}`: {e}")

    def process_data(self):
        dataframe = self.load_all_excel_from_folder()

        if not dataframe.empty:
            self.upsert_to_bigquery(dataframe)
            print("Dados carregados e atualizados com sucesso.")
        else:
            print("Nenhum dado encontrado para carregar.")











# gcs2bq/main.py
from gcs2bq import LoadXlsxToBigQuery

class Main:
    def __init__(self, bucket_name, folder_xlsx, sheet_name, dataset_id, table_id, unique_key_columns):
        self.bucket_name = bucket_name
        self.folder_xlsx = folder_xlsx
        self.sheet_name = sheet_name
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.unique_key_columns = unique_key_columns

    def load_xlsx_data(self):
        # Carregar XLSX
        xlsx_loader = LoadXlsxToBigQuery(self.bucket_name, self.folder_xlsx, self.sheet_name, self.dataset_id, self.table_id, self.unique_key_columns)
        xlsx_loader.process_data()

    def run(self):
        self.load_xlsx_data()

if __name__ == "__main__":
    # Evita execução direta do arquivo main.py
    print("Este script não deve ser executado diretamente. Use um arquivo separado para instanciar a classe e chamar o método `process_data`.")

