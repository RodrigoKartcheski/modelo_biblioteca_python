from gcs2bq import GcsToDataFrame, DataFrameToXlsx, BigQueryLoader  # Importação da nova classe
#from gcs2bq.cloud_function.gcs_xlsx_to_dataframe_reader import gcs_to_dataframe



class Main:
    def __init__(self, project_id: str, bucket_name: str, folder_xlsx: str, file_name: str, sheet_name: str, dataset_id: str, table_id: str, unique_key_columns: list):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.folder_xlsx = folder_xlsx
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.unique_key_columns = unique_key_columns


    def run(self):

        # 1️⃣ Carregar dados XLSX para GCS
        gcs_xlsx_loader = DataFrameToXlsx(self.project_id, self.bucket_name, self.folder_xlsx, self.file_name, self.sheet_name)
        dataframe_xlsx = gcs_xlsx_loader.load_excel_from_gcs()


        if dataframe_xlsx.empty:
            print("Nenhum dado encontrado no arquivo XLSX no GCS.")
            return
        
        print("Arquivo XLSX carregado com sucesso do GCS.")

        # Ler os arquivos do GCS e converter para DataFrame
        gcs_loader = GcsToDataFrame(self.bucket_name, self.folder_xlsx, self.sheet_name)
        dataframe = gcs_loader.load_all_excel_from_folder()

        # Exibir os dados carregados, se houver algum
        if not dataframe.empty:
            print("Dados carregados com sucesso:")
            print(dataframe)

            # Chamar a nova classe para carregar no BigQuery
            bq_loader = BigQueryLoader(self.project_id, self.dataset_id, self.table_id, self.unique_key_columns)
            bq_loader.upsert_to_bigquery(dataframe)
        else:
            print("Nenhum dado encontrado para carregar.")

if __name__ == "__main__":
    print("Este script não deve ser executado diretamente. Use um arquivo separado para instanciar a classe e chamar o método `run`.")
    

