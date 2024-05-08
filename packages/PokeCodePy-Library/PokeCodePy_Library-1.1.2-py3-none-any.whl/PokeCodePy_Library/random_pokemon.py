import pkg_resources
import pandas as pd

class RandomPokemon:
    FILE_PATH = pkg_resources.resource_filename(__name__, 'pokemon.csv')

    def __init__(self):
        self._file = pd.read_csv(RandomPokemon.FILE_PATH) #lee el archivo con pandas
        self._pokemon = None #Guarda todos los datos (columnas) del pokemon aleatorio
        self._number = None #Numero del pokemon
        self._name = None #Nombre del pokemon
        self._type1 = None #tipo 1 del pokemon
        self._type2 = None #tipo 2 del pokemon
        self._total = None #total
        self._hp = None #hp
        self._attack = None #ataque
        self._defense = None #defensa
        self._spatk = None
        self._spdef = None
        self._speed = None
        self._generation = None
        self._legendary = None

    def generate_random(self):
        self._pokemon = self._file.sample()
        self._number = self._pokemon["#"].values[0]
        self._name = self._pokemon["Name"].values[0]
        self._type1 = self._pokemon["Type 1"].values[0]
        self._type2 = self._pokemon["Type 2"].values[0]
        self._total = self._pokemon["Total"].values[0]
        self._hp = self._pokemon["HP"].values[0]
        self._attack = self._pokemon["Attack"].values[0]
        self._defense = self._pokemon["Defense"].values[0]
        self._spatk = self._pokemon["Sp.Atk"].values[0]
        self._spdef = self._pokemon["Sp. Def"].values[0]
        self._speed = self._pokemon["Speed"].values[0]
        self._generation = self._pokemon["Generation"].values[0]
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

    def getSpatk(self):
        return self._spatk

    def getSpdef(self):
        return self._spdef

    def getSpeed(self):
        return self._speed

    def getGeneration(self):
        return self._generation

    def getLegendary(self):
        return self._legendary


