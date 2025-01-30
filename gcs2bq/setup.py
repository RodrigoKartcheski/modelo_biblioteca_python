from setuptools import setup, find_packages

setup(
    name='gcs2bq',  # Nome do seu pacote
    version='0.0.18',
    description='Biblioteca para mover dados entre o Google Cloud Storage (GCS) e o BigQuery',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Seu Nome',
    author_email='seu_email@dominio.com',
    url='https://github.com/seu_usuario/gcs2bq',  # Atualize com o link do repositório
    packages=find_packages(),  # Encontrar pacotes automaticamente
    entry_points={
        'console_scripts': [
            'gcs2bq=gcs2bq.main:main',  # Atualize conforme necessário
        ]
    },
    install_requires=[
        'google-cloud-storage>=2.0.0',  # GCS
        'google-cloud-bigquery>=3.0.0',  # BigQuery
        'google-auth>=2.0.0',  # Autenticação
        'xlsxwriter==3.0.3', # manipular arquivos do formato .xlsx
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # ou GPL, conforme sua escolha
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
