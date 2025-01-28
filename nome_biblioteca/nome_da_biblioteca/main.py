import pandas as pd

class ConcatenadorDeColunas:
    @staticmethod
    def concatena(df: pd.DataFrame, col1: str, col2: str, separador: str = " ") -> pd.Series:
        """
        Concatena duas colunas de um DataFrame em uma nova coluna.
        
        :param df: DataFrame que contém as colunas a serem concatenadas.
        :param col1: Nome da primeira coluna a ser concatenada.
        :param col2: Nome da segunda coluna a ser concatenada.
        :param separador: Separador a ser usado entre os valores das colunas (padrão é espaço).
        :return: Uma Série com as colunas concatenadas.
        """
        if col1 not in df.columns or col2 not in df.columns:
            raise ValueError(f"As colunas {col1} e/ou {col2} não existem no DataFrame.")
        
        return df[col1].astype(str) + separador + df[col2].astype(str)
