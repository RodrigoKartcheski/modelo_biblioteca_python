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

############################################################################################################################

from gcs2bq import GcsToDataFrame, BigQueryLoader

# Defina os parâmetros necessários
project_id = "dataplex-experience-6133"
#
bucket_name = "bucket-6133-20241008_2"
bucket_folder = "folder"
sheet_name = "sua-aba"
#
dataset_id = "data_conjunto"
table_id = "table_id"
unique_key_columns = ["Concessao"]

# Carregar os dados do GCS usando a classe GcsToDataFrame
gcs_loader = GcsToDataFrame(project_id, bucket_name, bucket_folder, sheet_name)
dataframe = gcs_loader.load_all_excel_from_folder()

# Chamar a classe BigQueryLoader e carregar os dados no BigQuery
bq_loader = BigQueryLoader(project_id, dataset_id, table_id, unique_key_columns)
bq_loader.upsert_to_bigquery(dataframe)



############################################################################################################################
# Obrigatorio para usar o pacote
!pip install -i https://test.pypi.org/simple/ gcs2bq==0.0.18
# Obrigatorio para usar o carregamento do DF de xlsx para o bucket
!pip install xlsxwriter

import pandas as pd
from gcs2bq import DataFrameToXlsx

# Criando o DataFrame
df = pd.DataFrame({
    'Coluna1': [1, 2, 3],
    'Coluna2': ['A', 'B', 'C'],
    'Coluna3': [10.5, 20.7, 30.2]
})

# Parâmetros do GCS
project_id = "dataplex-experience-6133"
bucket_name = "bucket-6133-20241008_2"
bucket_folder = "folder"
file_name = "dados.xlsx"
sheet_name = "Dados"


# Instanciando a classe e salvando no GCS
DataFrameToXlsx(
    dataframe=df,  # ✅ Passando o DataFrame corretamente
    bucket_name=bucket_name,
    bucket_folder=bucket_folder,  # ✅ Nome correto do parâmetro
    file_name=file_name,
    sheet_name=sheet_name
).save_to_gcs()  # ✅ Nome correto do método de salvamento

print(f"Arquivo salvo no GCS: gs://{bucket_name}/{bucket_folder}/{file_name}")



############################################################################################################################



# Variaveis 

📌 Convenção de Nomes para Variáveis e Constantes
Seguir boas práticas na definição de nomes é essencial para garantir a consistência e legibilidade do código.

📝 Boas Práticas
✅ Variáveis comuns → Use snake_case (letras minúsculas, separadas por _)
✅ Constantes → Use UPPER_SNAKE_CASE (letras maiúsculas, separadas por _)

🔹 Exemplo de Nomeação
Se os valores não serão alterados no código (constantes):

python
Copiar
Editar
PROJECT_ID = "my-project"
BUCKET_NAME = "my-bucket"
DATASET_ID = "data_conjunto"
Se forem variáveis mutáveis (podem ser alteradas durante a execução):

python
Copiar
Editar
bucket_folder = "folder"
sheet_name = "sua-aba"
table_id = "table_id"
unique_key_columns = ["Concessao"]
⚡ Resumo
📍 Constantes → UPPER_SNAKE_CASE
📍 Variáveis mutáveis → snake_case

Seguir essas convenções ajuda a manter o código mais organizado, compreensível e padronizado. 🚀