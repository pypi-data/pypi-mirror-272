from setuptools import setup, find_packages

setup(

    name='BuscaTuPokemon',
    version='1.0.0',
    author= 'Milton Angel',
    author_email='milton_ac@tesch.edu.mx',
    description='Es una libreria la cual permitira generar un pokemon aleatorio',
    packages= ['BuscaTuPokemon'],
    package_data={'BuscaTuPokemon': ['pokemon.csv']},
    install_requires=['pandas',
                      'twine',
                      'wheel' ,
                      'setuptools'
                      ],
)

