from setuptools import setup, find_packages

setup(
    name='YoteelijSnorlax',
    version='1.0.1',
    author='Missael Angel Cardenas',
    author_email= 'missaelanggel@gmail.com',
    description= 'Una Biblioteca que contiene la clase Random_pokemon para mostranos poquemones locos',
    packages=["YoteelijSnorlax"],
    package_data= {'YoteelijSnorlax': ['pokemon.csv']},
    install_requires= [
        'pandas', 'pkg_resources', 'setuptools', 'twine', 'wheel',
    ],
)