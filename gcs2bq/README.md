# README.md

pip install -i https://test.pypi.org/simple/ gcs2bq==0.0.2

from gcs2bq import LoadXlsxToBigQuery

from gcs2bq import LoadXlsxToBigQuery


# Defina os parâmetros necessários
bucket_name = "bucket-6133-20241008_2"
bucket_folder = "folder"
sheet_name = "sua-aba"
dataset_id = "data_conjunto"
table_id = "table_id"
unique_key_columns = ["Concessao"]

# Instanciar a classe
processor = LoadXlsxToBigQuery(
    bucket_name=bucket_name,
    bucket_folder=bucket_folder,
    sheet_name=sheet_name,
    dataset_id=dataset_id,
    table_id=table_id,
    unique_key_columns=unique_key_columns
)

# Processar os dados

print(processor.process_data())