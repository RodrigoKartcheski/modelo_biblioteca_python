import unittest
import pandas as pd
from nome_biblioteca.nome_da_biblioteca.main import ConcatenadorDeColunas

class TestConcatenadorDeColunas(unittest.TestCase):

    def setUp(self):
        """
        Método que prepara o ambiente para os testes. 
        Criamos um DataFrame de exemplo para ser usado nos testes.
        """
        self.df = pd.DataFrame({
            'nome': ['João', 'Maria', 'Pedro'],
            'sobrenome': ['Silva', 'Oliveira', 'Santos']
        })
        self.concatenador = ConcatenadorDeColunas(self.df)

    def test_concatena_colunas(self):
        """
        Testa a concatenação de duas colunas.
        """
        resultado = self.concatenador.concatena('nome', 'sobrenome')
        esperado = pd.Series(['João Silva', 'Maria Oliveira', 'Pedro Santos'])
        pd.testing.assert_series_equal(resultado, esperado)

    def test_concatena_com_separador(self):
        """
        Testa a concatenação de duas colunas com um separador customizado.
        """
        resultado = self.concatenador.concatena('nome', 'sobrenome', separador=', ')
        esperado = pd.Series(['João, Silva', 'Maria, Oliveira', 'Pedro, Santos'])
        pd.testing.assert_series_equal(resultado, esperado)

    def test_coluna_nao_existe(self):
        """
        Testa o caso onde uma ou ambas as colunas não existem no DataFrame.
        """
        with self.assertRaises(ValueError):
            self.concatenador.concatena('nome', 'endereco')  # Coluna 'endereco' não existe.

    def test_concatena_colunas_vazias(self):
        """
        Testa a concatenação de colunas com valores vazios.
        """
        self.df['nome'] = [None, 'Maria', 'Pedro']
        resultado = self.concatenador.concatena('nome', 'sobrenome')
        esperado = pd.Series(['None Silva', 'Maria Oliveira', 'Pedro Santos'])
        pd.testing.assert_series_equal(resultado, esperado)

if __name__ == '__main__':
    unittest.main()
