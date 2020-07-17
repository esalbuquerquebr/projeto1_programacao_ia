"""
Classe que representa um estado de valor único

"""
from functools import reduce
class SingleValueState:

    def __init__(self, value, fitness):
        self._value = value
        self._fitness = fitness
    
    @property
    def value(self):
        return self._value

    @property
    def fitness(self):
        return self._fitness

    def is_better_than(self, other, min=True):
        if (min):
            return self._fitness < other.fitness if other and other.fitness else True
        else:
            return self._fitness > other.fitness if other and other.fitness else True

    def __hash__(self):
        return hash(self._value)

    def __eq__(self, other):
        return self._value == other.value

    def __ne__(self, other):
        return self._value != other.value

    def __lt__(self, other):
        return self._fitness < other._fitness

    def __le__(self, other):
        return self._fitness <= other._fitness

    def __ge__(self, other):
        return self._fitness >= other._fitness

    def __gt__(self, other):        
        return self._fitness > other._fitness
    
    def __str__(self):
        return f'value:{self.value} | fitness:{self.fitness}'