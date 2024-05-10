from setuptools import setup, find_packages

setup(
    name='POKE_DONPOLLO',
    version='2.0.5',
    author= "FernandoRoldan",
    author_email="roldanf661@gmail.com",
    description="LIBRERIA QUE GENRA UN POKEMON DE DONPOLLOLO, ES DECIR UN POKEMON ALEATORIO",
    packages=["POKE_DONPOLLO"],
    package_data= {'POKE_DONPOLLO': ['pokemon.csv']},
    install_requires = ['pandas']
)