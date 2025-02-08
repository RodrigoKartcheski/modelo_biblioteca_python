import pandas as pd
import pyarrow.parquet as pq
from google.cloud import storage
from io import BytesIO
from datetime import datetime
import pytz


class DataFrameToParquet:
    def __init__(self, dataframe: pd.DataFrame, bucket_name: str, bucket_folder: str):
        """
        Classe para salvar um DataFrame no GCS como um arquivo Parquet.
        
        :param dataframe: DataFrame a ser salvo
        :param bucket_name: Nome do bucket no GCS
        :param bucket_folder: Caminho/pasta dentro do bucket
        """
        self.dataframe = dataframe
        self.bucket_name = bucket_name
        self.bucket_folder = bucket_folder
        self.client = storage.Client()
        
        # Gera um nome de arquivo baseado no timestamp atual
        timezone = pytz.timezone('America/Sao_Paulo')
        self.file_name = datetime.now(tz=timezone).strftime("%d-%m-%yT%H:%M") + ".parquet"

    def save_to_gcs(self):
        """Salva o DataFrame como um arquivo Parquet no GCS"""
        if self.dataframe.empty:
            print("DataFrame vazio! Nenhum dado para salvar.")
            return

        # Criar um buffer de memória para armazenar o arquivo Parquet
        output = BytesIO()
        self.dataframe.to_parquet(output, engine='pyarrow', index=False)
        output.seek(0)

        # Caminho completo no bucket
        blob_path = f"{self.bucket_folder}/{self.file_name}"
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(blob_path)

        # Upload do arquivo para o GCS
        blob.upload_from_file(output, content_type='application/octet-stream')

        print(f"Arquivo salvo com sucesso no GCS: gs://{self.bucket_name}/{blob_path}")
        return self.file_name  # Retorna o nome do arquivo para referência futura
