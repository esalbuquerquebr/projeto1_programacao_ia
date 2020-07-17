"""
Classe que representa a busca local Hill Climbing (simples)

"""
from .abstract_algorithm import AbstractAlgorithm

class SimpleHillClimbing(AbstractAlgorithm):

    def __init__(self, fn_goal, fn_neighbor, fn_init_state, qtt_iter=1000, is_min=True):
        super().__init__(fn_goal, fn_neighbor, fn_init_state, qtt_iter, is_min)

    # Atualiza os estados vizinho, atual e melhor
    def _update_states(self, new_state):
        self.neighbor_state = new_state
        self.current_state = new_state if new_state.is_better_than(self.current_state, self.is_min) else self.current_state
        self.best_state = new_state if new_state.is_better_than(self.best_state, self.is_min) else self.best_state

