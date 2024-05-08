import pkg_resources
import pandas as pd

class RandomPokemon:
    FILE_PATH = pkg_resources.resource_filename(__name__, 'pokemon.csv')

    def __init__(self):
        self._file = pd.read_csv(RandomPokemon.FILE_PATH)
        self._pokemon = None
        self._number = None
        self._name = None
        self._type1 = None
        self._type2 = None
        self._total = None
        self._hp = None
        self._attack = None
        self._defense = None
        self._spatk = None
        self._spdef = None
        self._speed = None
        self._generation = None
        self._legendary = None

    def generate_random(self):
        self._pokemon = self._file. sample()
        self._number = self._pokemon["#"]. values[0]
        self._name = self._pokemon["Name"]. values[0]
        self._type1 = self._pokemon["Type 1"]. values[0]
        self._type2 = self._pokemon["Type 2"].values[0]
        self._total = self._pokemon["#"].values[0]
        self._hp = self._pokemon["#"].values[0]
        self._attack = self._pokemon["#"].values[0]
        self._defense = self._pokemon["#"].values[0]
        self._spatk = self._pokemon["#"].values[0]
        self._spdef = self._pokemon["#"].values[0]
        self._speed = self._pokemon["#"].values[0]
        self._generation = self._pokemon["#"].values[0]
        self._legendary = self._pokemon["Legendary"].values[0]

    def getPokemon(self):
       return self._pokemon

    def getNumber(self):
       return self._number

    def getName(self):
        return self._name

    def getType1(self):
        return self._type1


    def getType2(self):
        return self._type2


    def getTotal(self):
        return self._total


    def getHp(self):
        return self._hp

    def getAttack(self):
        return self._attack

    def getDefense(self):
        return self._defense

    def getSpAtk(self):
        return self._spatk

    def getSpdef(self):
        return self._spdef

    def getSpeed(self):
        return self._speed

    def getGeneration(self):
        return self._generation

    def getLegendary(self):
        return self._legendary









