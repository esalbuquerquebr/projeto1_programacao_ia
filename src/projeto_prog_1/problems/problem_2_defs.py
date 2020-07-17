"""
Módulo que representa algumas definições e funções para o problema 2


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
_VALID_INTERVAL = {'from': -5.12, 'to': 5.12}

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
FIXED_INIT_STATE_ARRAY = [[-3.996687, -4.152387], [-2.548739, -2.712921],
                        [-4.919496, -3.701581], [-4.152518, -5.693362], [-5.764245, -3.261190],
                        [4.741434, 3.587078], [3.396167, 2.053729], [4.554253, 2.603533],
                        [4.731824, 4.921208],[5.055210, 5.181399]]

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
def fn_goal(value):
    x = value[0]
    y = value[1]
    return 20 + ((x ** 2) - (10 * np.cos(2 * np.pi * x))) + ((y ** 2) - (10 * np.cos(2 * np.pi * x)))
        
def fn_neighbor(state, fn_goal, std = STANDARD_DEVIATION):
    # Função para geração de uma dimensão para geração de vizinhos do problema
    def fn_dim_neighbor(dim, std = STANDARD_DEVIATION):
        for iter in range(0, _QTT_ATTEMPS_GEN_NEIGHBOR):
            delta = np.random.normal(0, std)
            neighbor_value = dim + delta
            if fn_is_valid_state_value(neighbor_value):
                return neighbor_value

            delta *= -1
            neighbor_value = dim + delta
            if fn_is_valid_state_value(neighbor_value):
                return neighbor_value

        raise SystemError(f"Can't generate valid neighbor from {state.value}")
    x = fn_dim_neighbor(state.value[0], std)
    y = fn_dim_neighbor(state.value[1], std)
    return fn_gen_state((x, y), fn_goal)

# Função para definir o estado inicial.
def fn_gen_state(state_value, fn_goal):
    return SingleValueState(state_value, fn_goal(state_value))

# Função que determina se um estado é válido para o problema    
def fn_is_valid_state_value(state_value):
    return state_value >= _VALID_INTERVAL['from'] and state_value <= _VALID_INTERVAL['to'] if state_value else False 

# Função para definir o estado inicial.
def fn_init_state(exec_code):
    x = FIXED_INIT_STATE_ARRAY[exec_code - 1][0]
    y = FIXED_INIT_STATE_ARRAY[exec_code - 1][1]
    def fn_init(fn_goal):
        init_state = fn_gen_state((x, y), fn_goal)
        return (None, init_state, init_state)
    return fn_init

# Função para gerar estado inicial
def fn_random_state(current_state, fn_goal):
    x = np.random.uniform(_VALID_INTERVAL['from'], _VALID_INTERVAL['to'])
    y = np.random.uniform(_VALID_INTERVAL['from'], _VALID_INTERVAL['to'])
    return fn_gen_state((x, y), fn_goal)


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


        alfax_crossover = np.random.uniform()
        child1x_value = (f1.value[0] * alfax_crossover) + (f2.value[0] * (1 - alfax_crossover))
        child2x_value = (f2.value[0] * alfax_crossover) + (f1.value[0] * (1 - alfax_crossover))

        alfay_crossover = np.random.uniform()
        child1y_value = (f1.value[1] * alfay_crossover) + (f2.value[1] * (1 - alfay_crossover))
        child2y_value = (f2.value[1] * alfay_crossover) + (f1.value[1] * (1 - alfay_crossover))

        if fn_is_valid_state_value(child1x_value) and fn_is_valid_state_value(child1y_value):
            alfa_mutation = np.random.uniform()
            child1 = fn_gen_state((child1x_value, child1y_value), fn_goal)
            child1 = fn_neighbor(child1, fn_goal) if alfa_mutation < PROB_MUTATION else child1
            single_states.add(child1)

        if fn_is_valid_state_value(child2x_value) and fn_is_valid_state_value(child2y_value):
            alfa_mutation = np.random.uniform()
            child2 = fn_gen_state((child2x_value, child2y_value), fn_goal)
            child2 = fn_neighbor(child2, fn_goal) if alfa_mutation < PROB_MUTATION else child2
            single_states.add(child2)

    list_result = list(single_states)
    return fn_gen_state_ga(list_result[0:population_len])

# Função para definir o estado inicial para o GA.
def fn_init_state_ga(index):
    def fn_init(fn_goal):
        ref = FIXED_INIT_STATE_ARRAY[index-1]
        ref_state = fn_gen_state((ref[0], ref[1]), fn_goal)
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
