import pkg_resources
import pandas as pd


class SelectPokemon:
    FILE_PATH = pkg_resources.resource_filename(__name__,'pokemon.csv')

    def __init__(self):
        self._file = pd.read_csv(SelectPokemon.FILE_PATH) # nos lee el archivo
        self._pokemon = None
        self._number = None
        self._name = None
        self._type1 = None

    def gen_pokemon(self):
        self._pokemon = self._file.sample()
        self._number = self._pokemon["#"].values[0]
        self._name = self._pokemon["Name"].values[0]
        self._type1 = self._pokemon["Type 1"].values[0]

    def getPokmn(self):
        return self._pokemon

    def getNumb(self):
        return self._number

    def getNam(self):
        return self._name

    def getTyp1(self):
        return self._type1

