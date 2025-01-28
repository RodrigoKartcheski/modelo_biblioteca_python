#pip install -i https://test.pypi.org/simple/ nome-da-biblioteca==0.1.4

import nome_da_biblioteca




from nome_da_biblioteca import ConcatenadorDeColunas
import pandas as pd

df = pd.DataFrame({
    'col1': ['A', 'B', 'C'],
    'col2': ['1', '2', '3']
})

resultado = ConcatenadorDeColunas.concatena(df, 'col1', 'col2', separador="-")
print(resultado)
