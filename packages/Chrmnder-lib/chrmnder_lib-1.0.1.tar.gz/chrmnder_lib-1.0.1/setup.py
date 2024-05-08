from setuptools import setup, find_packages

setup(
    name='Chrmnder_lib',
    version='1.0.1',
    author='Missael Angel Cardenas',
    author_email= 'missaelanggel@gmail.com',
    description= 'Una Biblioteca que contiene la clase Random_pokemon para mostranos poquemones locos',
    packages=["Chrmnder_lib"],
    package_data={'Chrmnder_lib': ['pokemon.csv']},
    install_requires=[
        'pandas', 'setuptools', 'twine', 'wheel'
    ],
)