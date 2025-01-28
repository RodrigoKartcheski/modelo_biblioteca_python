from setuptools import setup, find_packages

setup(
    name='nome_da_biblioteca',
    version='0.1.4',
    description='Biblioteca para concatenar duas colunas de um DataFrame',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Seu Nome',
    author_email='seu_email@dominio.com',
    url='https://github.com/seu_usuario/nome_da_biblioteca',  # Atualize com o link do repositório
    packages=['nome_da_biblioteca'],
    entry_points={
        'console_scripts': [
            'nome_da_biblioteca=nome_da_biblioteca.main:main'
        ]
    },
    install_requires=[
        'pandas>=1.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # ou GPL, conforme sua escolha
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
