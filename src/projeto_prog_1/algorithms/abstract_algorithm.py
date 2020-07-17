"""
Classe que representa um algoritmo de otimização abstrato

"""
from abc import ABCMeta, abstractmethod, abstractproperty

class AbstractAlgorithm(metaclass=ABCMeta):

    def __init__(self, fn_goal, fn_neighbor, fn_init_state, qtt_iter=1000, is_min=True):
        super().__init__()
        self.fn_goal = fn_goal
        self.fn_neighbor = fn_neighbor
        self.fn_init_state = fn_init_state
        self.qtt_iter = qtt_iter
        self.is_min = is_min

        self.neighbor_state = None
        self.current_state = None
        self.best_state = None

        self.iteration = 0
        
    # Inicializa os estados do algoritmo
    def _init(self):
        (self.neighbor_state, self.current_state, self.best_state) = self.fn_init_state(self.fn_goal)
        return (self.neighbor_state, self.current_state, self.best_state)

    # Retorna o iterador
    def __iter__(self):
        return self

    # Executa uma iteração do algoritmo
    def __next__(self):
        self.iteration += 1
        if self.iteration == 1:
            return self._init()

        if self.iteration > self.qtt_iter:
            raise StopIteration()        

        # Produz o novo vizinho e atualiza o estado
        neighbor_state = self.fn_neighbor(self.current_state, self.fn_goal)
        #neighbor_state = self.fn_gen_state(neighbor, self.fn_goal)
        self._update_states(neighbor_state)
        return (self.neighbor_state, self.current_state, self.best_state)

    # Atualiza os estados vizinho, atual e melhor
    @abstractmethod
    def _update_states(self, new_state):
        pass

    # Retorna o dicionario com a iteração e melhor estado
    def to_dict(self):
        return {
            'algorithm': self.__class__.__name__,
            'iteration': self.iteration,
            'best_state_value': self.best_state.value,
            'best_state_fitness': self.best_state.fitness
        }



