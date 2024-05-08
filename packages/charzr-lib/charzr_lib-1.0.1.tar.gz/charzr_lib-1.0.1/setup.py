from setuptools import setup, find_packages

setup(
    name='charzr_lib',
    version='1.0.1',
    author='Missael Angel Cardenas',
    author_email= 'missaelanggel@gmail.com',
    description= 'Una Biblioteca que contiene la clase Random_pokemon para mostranos poquemones locos',
    packages=["charzr_lib"],
    package_data= {'charzr_lib': ['pokemon.csv']},
    install_requires= [
        'pandas', 'pkg_resources', 'setuptools', 'twine', 'wheel',
    ],
)