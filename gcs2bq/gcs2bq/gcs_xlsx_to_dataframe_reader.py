from google.cloud import storage
import pandas as pd
from io import BytesIO

class GcsToDataFrame:
    """
    Classe para carregar arquivos Excel armazenados em uma pasta específica dentro de um bucket no Google Cloud Storage (GCS)
    e consolidá-los em um único DataFrame do pandas.
    """
    def __init__(self, project_id: str, bucket_name: str, folder_name: str, sheet_name: str):
        """
        Inicializa a classe com as informações do bucket, pasta e aba da planilha.

        :param bucket_name: Nome do bucket no Google Cloud Storage.
        :param folder_name: Nome da pasta dentro do bucket.
        :param sheet_name: Nome da aba da planilha a ser lida.
        """
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.folder_name = folder_name
        self.sheet_name = sheet_name
        self.storage_client = storage.Client(project=self.project_id)

    def load_all_excel_from_folder(self) -> pd.DataFrame:
        """
        Lista e lê todos os arquivos Excel (.xlsx) de uma pasta específica no GCS e os consolida em um único DataFrame.

        :return: DataFrame consolidado contendo os dados de todas as planilhas carregadas.
        """
        folder_path_bucket = f"{self.folder_name}/"
        blobs = self.storage_client.list_blobs(self.bucket_name, prefix=folder_path_bucket)

        dataframes = []
        for blob in blobs:
            try:
                # Verifica se o arquivo é um Excel (.xlsx)
                if blob.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    print(f"Lendo arquivo: {blob.name}")
                    
                    # Faz o download do arquivo como bytes
                    content = blob.download_as_bytes()
                    
                    # Lê o arquivo Excel e adiciona ao DataFrame
                    df = pd.read_excel(BytesIO(content), sheet_name=self.sheet_name)
                    dataframes.append(df)
            except Exception as e:
                print(f"Erro ao processar o arquivo {blob.name}: {e}")

        # Retorna a concatenação de todos os DataFrames ou um DataFrame vazio caso nenhum arquivo tenha sido lido
        return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()
