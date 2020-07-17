"""
Módulo que representa algumas definições e funções para o problema 3


"""
import numpy as np
import csv
import os.path
from functools import reduce
from scipy.spatial import distance
from algorithms.state.single_value_state import SingleValueState
from algorithms.state.mult_value_state import MultValueState


TOY_5_CITIES = {
    1: (9.340596780273533, 0.944644983514447),
    2: (9.453687199297686, 4.296319873487294),
    3: (3.954576491945417, -5.678210088392472),
    4: (9.525489095524836, -9.875394895908203),
    5: (-4.940352752331121, -1.304169351911085)
}
         
TOY_10_CITIES = {
    1: (0.9701402142106161, 0.8797074102376001),
    2: (8.181770830879042, 7.0846248063834025),
    3: (-0.07712137750422343, 3.9721858910577694),
    4: (3.733371632055352, 6.6998510725052185),
    5: (2.1421261194286583, -2.54738692880877),
    6: (-2.220915673767035, -4.112497129729418),
    7: (0.15908796673666892, 7.5403803382850825),
    8: (-8.276413817305874, 6.208957261216149),
    9: (-3.0288821940271156, 3.510752587262811),
    10: (6.703035457463709, -5.079996439520553)    
}


TOY_38_CITIES = {
    1: (11003.611100,42102.500000),
    2: (11108.611100,42373.888900),
    3: (11133.333300,42885.833300),
    4: (11155.833300,42712.500000),
    5: (11183.333300,42933.333300),
    6: (11297.500000,42853.333300),
    7: (11310.277800,42929.444400),
    8: (11416.666700,42983.333300),
    9: (11423.888900,43000.277800),
    10: (11438.333300,42057.222200),
    11: (11461.111100,43252.777800),
    12: (11485.555600,43187.222200),
    13: (11503.055600,42855.277800),
    14: (11511.388900,42106.388900),
    15: (11522.222200,42841.944400),
    16: (11569.444400,43136.666700),
    17: (11583.333300,43150.000000),
    18: (11595.000000,43148.055600),
    19: (11600.000000,43150.000000),
    20: (11690.555600,42686.666700),
    21: (11715.833300,41836.111100),
    22: (11751.111100,42814.444400),
    23: (11770.277800,42651.944400),
    24: (11785.277800,42884.444400),
    25: (11822.777800,42673.611100),
    26: (11846.944400,42660.555600),
    27: (11963.055600,43290.555600),
    28: (11973.055600,43026.111100),
    29: (12058.333300,42195.555600),
    30: (12149.444400,42477.500000),
    31: (12286.944400,43355.555600),
    32: (12300.000000,42433.333300),
    33: (12355.833300,43156.388900),
    34: (12363.333300,43189.166700),
    35: (12372.777800,42711.388900),
    36: (12386.666700,43334.722200),
    37: (12421.666700,42895.555600),
    38: (12645.000000, 42973.333300)

}

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
QTT_ITERATION_RESTART = 250

# Pecentual do total para retornar valor constante na fn de probabilidade do SA
# 90%
PERCENT_ITER_SA = 0.65

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

# Pontos para o problema TSP a ser utlizado na fn_goal
PROBLEM_POINTS = TOY_38_CITIES

PROBLEM_LEN = len(PROBLEM_POINTS)

# Função objetivo
# Função a ser minimizada
def fn_goal(value):
    d_going = 0
    qtt_points = len(value)
    for i in range(0, qtt_points):
        i_next = i + 1
        if i_next < qtt_points:
            d_going += distance.euclidean(PROBLEM_POINTS[value[i]], PROBLEM_POINTS[value[i_next]])
    d_back = distance.euclidean(PROBLEM_POINTS[value[-1]], PROBLEM_POINTS[value[0]])
    return d_going + d_back


# Função para geração de vizinhos do problema
def fn_neighbor(state, fn_goal):
    qtt_points = len(state.value)
    new_state_value = list(state.value)
    index_i = np.random.randint(0, qtt_points)
    index_j = index_i
    while index_j == index_i:
        index_j = np.random.randint(0, qtt_points)
    new_state_value[index_i], new_state_value[index_j] = new_state_value[index_j], new_state_value[index_i]
    return fn_gen_state(new_state_value, fn_goal)

# Função para definir o estado inicial.
def fn_gen_state(state_value, fn_goal):
    return SingleValueState(state_value, fn_goal(state_value))

# Função para definir o estado inicial.
def fn_init_state(exec_code):
    def random_seq(n, i):
        #seed_for_rerandomization = np.random.randint(0, 1e6)
        np.random.seed(i)
        solucao_inicial = np.random.permutation(range(1, n+1))
        np.random.seed()
        return list(solucao_inicial)
    state_value = list(random_seq(PROBLEM_LEN, exec_code))
    def fn_init(fn_goal):
        init_state = fn_gen_state(state_value, fn_goal)
        return (None, init_state, init_state)
    return fn_init

# Função para gerar estado inicial
def fn_random_state(current_state, fn_goal):
    def random_seq(n):
        np.random.seed()
        solucao = np.random.permutation(range(1, n+1))
        return list(solucao)
    new_state = list(random_seq(len(current_state.value)))
    return fn_gen_state(new_state, fn_goal)

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

    def ox_crossover1p(f1, f2):
        f1_sequence = f1.value['sequence']
        f2_sequence = f2.value['sequence']
        point_cut = np.random.randint(0, len(f1_sequence))
        rad_1 = f1_sequence[:point_cut]
        rad_2 = f2_sequence[:point_cut]

        order_1 = (f1_sequence[point_cut:] + f1_sequence[:point_cut])[::-1]
        order_2 = (f2_sequence[point_cut:] + f2_sequence[:point_cut])[::-1]

        qtt_sufix = len(f1_sequence) - point_cut
        while qtt_sufix > 0:
            c2 = order_2.pop()
            if c2 not in rad_1:
                rad_1.append(c2)
                qtt_sufix -= 1

        qtt_sufix = len(f1_sequence) - point_cut
        while qtt_sufix > 0:
            c1 = order_1.pop()
            if c1 not in rad_2:
                rad_2.append(c1)
                qtt_sufix -= 1

        return rad_1, rad_2        

        
    def ox_crossover2p(f1_sequence, f2_sequence):
        qtt_points = len(f1_sequence)

        fist_point_cut = np.random.randint(0, qtt_points)
        second_point_cut = fist_point_cut
        while fist_point_cut == second_point_cut:
            second_point_cut = np.random.randint(0, qtt_points)

        # Ajuste de indices (menor primeiro)
        if fist_point_cut > second_point_cut:
            fist_point_cut, second_point_cut = second_point_cut, fist_point_cut 

        rad_1 = f1_sequence[fist_point_cut:second_point_cut]
        rad_2 = f2_sequence[fist_point_cut:second_point_cut]

        order_1 = (f1_sequence[second_point_cut:] + f1_sequence[:fist_point_cut] + list(rad_1))[::-1]
        order_2 = (f2_sequence[second_point_cut:] + f2_sequence[:fist_point_cut] + list(rad_2))[::-1]

        qtt_sufix = qtt_points - second_point_cut
        while qtt_sufix > 0:
            c2 = order_2.pop()
            if c2 not in rad_1:
                rad_1.append(c2)
                qtt_sufix -= 1

        qtt_sufix = qtt_points - second_point_cut
        while qtt_sufix > 0:
            c1 = order_1.pop()
            if c1 not in rad_2:
                rad_2.append(c1)
                qtt_sufix -= 1
        
        qtt_prefix = qtt_points - len(rad_1)
        while qtt_prefix > 0:
            c2 = order_2.pop()
            if c2 not in rad_1:
                rad_1 = [c2] + rad_1
                qtt_prefix -= 1

        qtt_prefix = qtt_points - len(rad_2)
        while qtt_prefix > 0:
            c1 = order_1.pop()
            if c1 not in rad_2:
                rad_2 = [c1] + rad_2
                qtt_prefix -= 1
        return rad_1, rad_2        

    single_states = [] #set()
    population_len = population.lenght
    first_fathers = int(population_len * 0.20)
    second_fathers = population_len
    #fit_adj = list(map(lambda f: f, population.fitnesses))
    #fit_adj_total = reduce(lambda a, f: f + a, fit_adj)
    #probs = list(map(lambda f: (f / fit_adj_total), fit_adj))[::-1]

    while len(single_states) < population_len:

        #p1 = np.random.uniform()
        #f1 = population.get_at(get_index_of_prob(p1, probs))
        i1_1 = np.random.randint(0, first_fathers)
        i1_2 = np.random.randint(0, first_fathers)
        #print("i1", i1)
        f1_1 = population.get_at(i1_1)
        f1_2 = population.get_at(i1_2)
        f1 = f1_1 if f1_1.is_better_than(f1_2) else f1_2

        #p2 = np.random.uniform()
        #f2 = population.get_at(get_index_of_prob(p2, probs))
        i2_1 = np.random.randint(0, second_fathers)
        i2_2 = np.random.randint(0, second_fathers)
        f2_1 = population.get_at(i2_1)
        f2_2 = population.get_at(i2_2)
        f2 = f2_1 if f2_1.is_better_than(f2_2) else f2_2

        #print("i2", i2)
 
        c1_seq, c2_seq = ox_crossover2p(f1.value, f2.value)
        
        child1 = fn_gen_state(c1_seq, fn_goal)
        alfa_mutation_c1 = np.random.uniform()
        child1 = fn_neighbor(child1, fn_goal) if alfa_mutation_c1 < PROB_MUTATION else child1
        single_states.append(child1)

        child2 = fn_gen_state(c2_seq, fn_goal)
        alfa_mutation_c2 = np.random.uniform()
        child2 = fn_neighbor(child2, fn_goal) if alfa_mutation_c2 < PROB_MUTATION else child2
        single_states.append(child2)

    list_result = list(single_states)
    return fn_gen_state_ga(list_result[0:population_len])


# Função para definir o estado inicial.
def fn_init_state_ga(exec_code):
    def random_seq(n, i):
        np.random.seed(i)
        solucao_inicial = np.random.permutation(range(1, n+1))
        np.random.seed()
        return list(solucao_inicial)
    def fn_init(fn_goal):
        sequence = random_seq(PROBLEM_LEN, exec_code)
        ref_state = fn_gen_state(sequence, fn_goal)
        single_states = [ref_state]
        while len(single_states) < POPULATION_LENGHT_GA:
            new_state = fn_random_state(ref_state, fn_goal)
            single_states.append(new_state)
        state = fn_gen_state_ga(single_states)
        return (None, state, state.best)

    return fn_init    

# Função para gerar um estado para o GA
def fn_gen_state_ga(values):
    return MultValueState(values)

