"""
Módulo que representa algumas definições e funções para o problema 1


"""
import numpy as np
import csv
import os.path
from functools import reduce
from algorithms.state.single_value_state import SingleValueState
from algorithms.state.mult_value_state import MultValueState

# Desvio padrão utilizado para geração de vizinhos.
STANDARD_DEVIATION = 2.0

# Intervalo válido para o problema
_VALID_INTERVAL = {'from': -100, 'to': 100}

# Quantidades de tentativas para geração de vizinhos válidos
# Utilizado pela função de geração de vizinhos
_QTT_ATTEMPS_GEN_NEIGHBOR = 200

# Tipo do objetivo.
# True = minimização | False = maximização
IS_MINIMIZATION = True

# Quantidade de execuções.
# O valor influencia a dimensão do array inicialização com valores fixos. FIXED_INIT_STATE_ARRAY
QTT_EXEC = 10

# Quantidade de iterações
QTT_ITERATION = 1000

# Quantidade de iterações para restart do HillClimbing
QTT_ITERATION_RESTART = 50

# Em caso de iniciar de um ponto fixo, setar a array de valores na variável fixed_init_state_array
# O array deve conter 10 valores referentes às 10 iterações
FIXED_INIT_STATE_ARRAY = [-88.42356534,-74.17652733,-96.04533575,-46.20975576,-51.08525224,84.25824009,89.62662973,62.71057724,41.82046817,74.48850765]

# Pecentual do total para retornar valor constante na fn de probabilidade do SA
# 90%
PERCENT_ITER_SA = 0.9

# Valor constante da probabilidade após o limite de iterações do SA
CONST_VALUE_SA = 0.0

# Quantidade de iterações para o GA
QTT_ITERATION_GA = 50

# Tamanho da população do GA
POPULATION_LENGHT_GA = 20

# Tamanho da população do GA
PROB_MUTATION = 0.3

# Header do CSV para todos os problemas
CSV_HEADER = ['algorithm', 'execution_code', 'iteration', 'best_state_value', 'best_state_fitness']    

# Função objetivo
# Função a ser minimizada
def fn_goal(x):
    return (x ** 2 / 100) + (10 * np.sin(x - (np.pi / 2)))
        
# Função para geração de vizinhos do problema
def fn_neighbor(state, fn_goal, std=STANDARD_DEVIATION):
    for iter in range(0, _QTT_ATTEMPS_GEN_NEIGHBOR):
        delta = np.random.normal(0, std)
        neighbor_value = state.value + delta
        if fn_is_valid_state_value(neighbor_value):
            return fn_gen_state(neighbor_value, fn_goal)

        delta *= -1
        neighbor_value = state.value + delta
        if fn_is_valid_state_value(neighbor_value):
            return fn_gen_state(neighbor_value, fn_goal)

    raise SystemError(f"Can't generate valid neighbor from {state.value}")

# Função que determina se um estado é válido para o problema    
def fn_is_valid_state_value(state_value):
    return state_value >= _VALID_INTERVAL['from'] and state_value <= _VALID_INTERVAL['to'] if state_value else False 

# Função para definir o estado inicial.
def fn_init_state(exec_code):
    state_value = FIXED_INIT_STATE_ARRAY[exec_code - 1]
    def fn_init(fn_goal):
        init_state = fn_gen_state(state_value, fn_goal)
        return (None, init_state, init_state)
    return fn_init

# Função para definir o estado inicial.
def fn_gen_state(state_value, fn_goal):
    return SingleValueState(state_value, fn_goal(state_value))

# Função para gerar estado inicial
def fn_random_state(current_state, fn_goal):
    value_state = np.random.uniform(_VALID_INTERVAL['from'], _VALID_INTERVAL['to'])
    return fn_gen_state(value_state, fn_goal)


# Função para gerar a função de calculo da 'temperatura' para o SA
def fn_calculate_prob_sa(qtt_iter, percent_iter, out_value):
    def fn_calculate_prob_sa(iteration):
        max_limit = qtt_iter * percent_iter
        if (iteration >= max_limit):
            return out_value
        else:
            return (max_limit - iteration) / max_limit
    return fn_calculate_prob_sa

def fn_neighbor_ga(population, fn_goal):
    def get_index_of_prob(prob, probs):
        acc = 0
        for i in range(0, len(probs)):
            acc += probs[i]
            if acc >= prob:
                return i
        return 0
    single_states = set()
    population_len = population.lenght
    fit_adj = list(map(lambda f: f + 10.000000000000000, population.fitnesses))
    fit_adj_total = reduce(lambda a, f: f + a, fit_adj)
    probs = list(map(lambda f: (f / fit_adj_total), fit_adj))[::-1]

    while len(single_states) < population_len:

        p1 = np.random.uniform()
        f1 = population.get_at(get_index_of_prob(p1, probs))

        p2 = np.random.uniform()
        f2 = population.get_at(get_index_of_prob(p2, probs))

        alfa_crossover = np.random.uniform()

        child1_value = (f1.value * alfa_crossover) + (f2.value * (1 - alfa_crossover))
        if fn_is_valid_state_value(child1_value):
            child1 = fn_gen_state(child1_value, fn_goal)
            alfa_mutation_c1 = np.random.uniform()
            child1 = fn_neighbor(child1, fn_goal) if alfa_mutation_c1 < PROB_MUTATION else child1
            single_states.add(child1)

        child2_value = (f2.value * alfa_crossover) + (f1.value * (1 - alfa_crossover))
        if fn_is_valid_state_value(child2_value):
            child2 = fn_gen_state(child2_value, fn_goal)
            alfa_mutation_c2 = np.random.uniform()
            child2 = fn_neighbor(child2, fn_goal) if alfa_mutation_c2 < PROB_MUTATION else child2
            single_states.add(child2)

    list_result = list(single_states)
    return fn_gen_state_ga(list_result[0:population_len])

# Função para definir o estado inicial para o GA.
def fn_init_state_ga(index):
    def fn_init(fn_goal):
        ref = FIXED_INIT_STATE_ARRAY[index-1]
        ref_state = fn_gen_state(ref, fn_goal)
        single_states = [ref_state]
        while len(single_states) < POPULATION_LENGHT_GA:
            new_state = fn_random_state(ref_state, fn_goal)
            if ref_state.is_better_than(new_state):
                single_states.append(new_state)

        state = fn_gen_state_ga(single_states)
        return (None, state, state.best)
    return fn_init

# Função para gerar um estado para o GA
def fn_gen_state_ga(values):
    return MultValueState(values)
