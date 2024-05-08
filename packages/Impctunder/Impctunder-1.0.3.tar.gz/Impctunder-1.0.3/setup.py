from setuptools import setup, find_packages

setup(
    name='Impctunder',
    version='1.0.3',
    author='Missael Angel Cardenas',
    author_email= 'missaelanggel@gmail.com',
    description= 'Una Biblioteca que contiene la clase Random_pokemon para mostranos poquemones locos',
    packages=["Impctunder"],
    package_data= {'Impctunder': ['pokemon.csv']},
    install_requires= [
        'pandas', 'pkg_resources', 'setuptools', 'twine', 'wheel',
    ],
)