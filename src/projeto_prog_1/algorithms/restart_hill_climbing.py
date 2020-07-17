"""
Classe que representa a busca local Hill Climbing com restart

"""
from .abstract_algorithm import AbstractAlgorithm

class RestartHillClimbing(AbstractAlgorithm):

    def __init__(self, fn_goal, fn_neighbor, fn_init_state, qtt_iter=1000, is_min=True, fn_random_state=None, qtt_iter_restart=50):
        self.fn_random_state = fn_random_state
        self.qtt_iter_restart = qtt_iter_restart
        super().__init__(fn_goal, fn_neighbor, fn_init_state, qtt_iter, is_min)


    # Executa o restart
    def _restart(self):
        restart_state = self.fn_random_state(self.current_state, self.fn_goal)
        #restart_state = self.fn_gen_state(restart_state_value, self.fn_goal)

        self.neighbor_state = None
        self.current_state = restart_state
        self.best_state = restart_state if restart_state.is_better_than(self.best_state) else self.best_state

    # Executa uma iteração do algoritmo
    def __next__(self):
        # Produz o restart se necessário
        if self.iteration > 1 and self.iteration % self.qtt_iter_restart == 0:
            self._restart()
        return super().__next__()
        
    # Atualiza os estados vizinho, atual e melhor
    def _update_states(self, new_state):
        self.neighbor_state = new_state
        self.current_state = new_state if new_state.is_better_than(self.current_state, self.is_min) else self.current_state
        self.best_state = new_state if new_state.is_better_than(self.best_state, self.is_min) else self.best_state

