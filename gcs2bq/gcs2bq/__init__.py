# gcs2bq/__init__.py
#from .load_xlsx_to_bigquery_02 import LoadXlsxToBigQuery  # Corrigido para importar apenas uma vez.
# gcs2bq/__init__.py

# Importação corrigida para garantir que GcsToDataFrame seja carregada corretamente.
from .gcs_xlsx_to_dataframe import GcsToDataFrame
from .bq_dataframe_loader import BigQueryLoader

