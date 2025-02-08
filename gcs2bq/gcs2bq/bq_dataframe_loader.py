import os
import requests
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from .def_get_gcp_service import get_gcp_service # Importa a função corretamente

class BigQueryLoader:
    def __init__(self, project_id, dataset_id, table_id, unique_key_columns):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.unique_key_columns = unique_key_columns
        self.bigquery_client = bigquery.Client()

    def ensure_table_exists(self, dataframe):
        table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

        try:
            table = self.bigquery_client.get_table(table_id)
            print(f"Tabela `{self.table_id}` já existe.")

            # Obtém o nome do serviço e configura os labels automaticamente
            service_name = get_gcp_service()  # Chama a função diretamente

            labels = {"etl-service": service_name}
            table.labels = labels

            table = self.bigquery_client.update_table(table, ["labels"])
            print(f"Labels da tabela `{self.table_id}` atualizados: {table.labels}")

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

            table = bigquery.Table(table_id, schema=schema)
            table.labels = {"origem_carga": get_gcp_service()}  # Chama a função diretamente
            self.bigquery_client.create_table(table)
            print(f"Tabela `{self.table_id}` criada com labels: {table.labels}")

        except Exception as e:
            print(f"Erro ao verificar/criar a tabela `{self.table_id}`: {e}")

    def upsert_to_bigquery(self, dataframe):
        self.ensure_table_exists(dataframe)
        table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

        try:
            query = f"SELECT {', '.join(self.unique_key_columns)} FROM `{table_id}`"
            existing_keys = self.bigquery_client.query(query).to_dataframe()

            merged_df = dataframe.merge(existing_keys, on=self.unique_key_columns, how='left', indicator=True)
            new_records = merged_df[merged_df['_merge'] == 'left_only'].drop(columns='_merge')

            if not new_records.empty:
                job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
                job = self.bigquery_client.load_table_from_dataframe(new_records, table_id, job_config=job_config)
                job.result()
                print(f"{len(new_records)} novos registros inseridos.")
            else:
                print("Nenhum novo registro para adicionar.")
        except Exception as e:
            print(f"Erro ao realizar o upsert na tabela `{self.table_id}`: {e}")
