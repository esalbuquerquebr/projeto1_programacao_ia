"""
Classe que representa um estado contendo uma população de valores simples

"""
from functools import reduce

class MultValueState:

    def __init__(self, single_states):
        self._states = sorted(single_states)

    @property
    def states(self):
        return self._states

    @property
    def lenght(self):
        return len(self._states)
    
    @property
    def best(self):
        if (self._states):
            return reduce(lambda b, s: b if b.is_better_than(s) else s, self._states)
        else:
            return None

    @property
    def fitness(self):
        return self.best.fitness

    @property
    def values(self):
        return list(map(lambda v: v.value, self._states))

    @property
    def fitnesses(self):
        return list(map(lambda v: v.fitness, self._states))
        
    def get_at(self, i):
        return self._states[i]

    