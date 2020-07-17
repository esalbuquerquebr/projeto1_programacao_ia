"""
Classe que representa o Algoritmo Genetico

"""
from .abstract_algorithm import AbstractAlgorithm

class GeneticAlgorithm(AbstractAlgorithm):
    def __init__(self, fn_goal, fn_neighbor, fn_init_state, qtt_iter=1000, is_min=True):
        super().__init__(fn_goal, fn_neighbor, fn_init_state, qtt_iter, is_min)

    # Atualiza os estados vizinho, atual e melhor
    def _update_states(self, new_state):
        #self.neighbor_state = new_state
        self.current_state = new_state
        new_state_best = new_state.best
        self.best_state = new_state_best if new_state_best.is_better_than(self.best_state, self.is_min) else self.best_state
    
   