"""
Classe que representa Simulated Annealing

"""
import numpy as np
from .abstract_algorithm import AbstractAlgorithm

class SimulatedAnnealing(AbstractAlgorithm):

    def __init__(self, fn_goal, fn_neighbor, fn_init_state, qtt_iter=1000, is_min=True, fn_calculate_prob_sa=None):
        super().__init__(fn_goal, fn_neighbor, fn_init_state, qtt_iter, is_min)
        self.fn_calculate_prob_sa = fn_calculate_prob_sa

    # Atualiza os estados vizinho, atual e melhor
    def _update_states(self, new_state):
        self.neighbor_state = new_state
        if (new_state.is_better_than(self.current_state)):
            self.current_state = new_state
        else:
            self.current_state = new_state if self.fn_calculate_prob_sa(self.iteration) > np.random.uniform() else self.current_state
        self.best_state = new_state if new_state.is_better_than(self.best_state, self.is_min) else self.best_state

