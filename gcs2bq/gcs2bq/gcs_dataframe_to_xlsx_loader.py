import pandas as pd
from google.cloud import storage
from io import BytesIO


class DataFrameToXlsx:
    def __init__(self, dataframe: pd.DataFrame, bucket_name: str, bucket_folder: str, file_name: str, sheet_name: str):
        """
        Classe para salvar um DataFrame no GCS como um arquivo XLSX.
        
        :param dataframe: DataFrame a ser salvo
        :param bucket_name: Nome do bucket no GCS
        :param bucket_folder: Caminho/pasta dentro do bucket
        :param file_name: Nome do arquivo a ser salvo
        :param sheet_name: Nome da aba no arquivo Excel
        """
        self.dataframe = dataframe
        self.bucket_name = bucket_name
        self.bucket_folder = bucket_folder
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.client = storage.Client()

    def save_to_gcs(self):
        """Salva o DataFrame como um arquivo XLSX no GCS"""
        if self.dataframe.empty:
            print("DataFrame vazio! Nenhum dado para salvar.")
            return

        # Criar um buffer de memória para armazenar o arquivo Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            self.dataframe.to_excel(writer, sheet_name=self.sheet_name, index=False)
        output.seek(0)

        # Caminho completo no bucket
        blob_path = f"{self.bucket_folder}/{self.file_name}"
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(blob_path)

        # Upload do arquivo para o GCS
        blob.upload_from_file(output, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        print(f"Arquivo salvo com sucesso no GCS: gs://{self.bucket_name}/{blob_path}")
