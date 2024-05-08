from setuptools import setup, find_packages

setup(
    name='ElijeTuPok',
    version='1.0.2',
    author='Missael Angel Cardenas',
    author_email= 'missaelanggel@gmail.com',
    description= 'Una Biblioteca que contiene la clase Random_pokemon para mostranos poquemones locos',
    packages=["ElijeTuPok"],
    package_data= {'ElijeTuPok': ['pokemon.csv']},
    install_requires= [
        'pandas', 'pkg_resources', 'setuptools', 'twine', 'wheel',
    ],
)