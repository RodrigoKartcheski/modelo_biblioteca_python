from google.cloud import bigquery
from google.api_core.exceptions import NotFound

class BigQueryLoader:
    def __init__(self, project_id, dataset_id, table_id, unique_key_columns):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.unique_key_columns = unique_key_columns
        self.bigquery_client = bigquery.Client(project=self.project_id)  # Agora usa project_id

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
            query = f"SELECT {', '.join(self.unique_key_columns)} FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`"
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