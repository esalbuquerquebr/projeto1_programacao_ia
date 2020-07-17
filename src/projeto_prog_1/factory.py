"""
Módulo para factory de algoritimos de otimização

"""
import problems.problem_1_defs as defs1
import problems.problem_2_defs as defs2
import problems.problem_3_defs as defs3
from algorithms.simple_hill_climbing import SimpleHillClimbing
from algorithms.restart_hill_climbing import RestartHillClimbing
from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.genetic_algorithm import GeneticAlgorithm

def get_defs(problem_number):
    if problem_number == 1:
        return defs1
    elif problem_number == 2:
        return defs2
    elif problem_number == 3:
        return defs3
    else:
        return None

def factory_simple_hillclimbing(defs):
    def fn_factory(exec_code):
        return SimpleHillClimbing(defs.fn_goal, defs.fn_neighbor, defs.fn_init_state(exec_code), qtt_iter=defs.QTT_ITERATION, is_min=defs.IS_MINIMIZATION)
    return fn_factory

def factory_restart_hillclimbing(defs):
    def fn_factory(exec_code):
        return RestartHillClimbing(defs.fn_goal, defs.fn_neighbor, defs.fn_init_state(exec_code), qtt_iter=defs.QTT_ITERATION, is_min=defs.IS_MINIMIZATION,
            fn_random_state=defs.fn_random_state,
            qtt_iter_restart=defs.QTT_ITERATION_RESTART)
    return fn_factory
    
def factory_simulated_annealing(defs):
    def fn_factory(exec_code):
        return SimulatedAnnealing(defs.fn_goal, defs.fn_neighbor, defs.fn_init_state(exec_code), qtt_iter=defs.QTT_ITERATION, is_min=defs.IS_MINIMIZATION,
            fn_calculate_prob_sa=defs.fn_calculate_prob_sa(defs.QTT_ITERATION, defs.PERCENT_ITER_SA, defs.CONST_VALUE_SA))
    return fn_factory

def factory_genetic_algorithm(defs):
    def fn_factory(exec_code):
        return GeneticAlgorithm(defs.fn_goal, defs.fn_neighbor_ga, defs.fn_init_state_ga(exec_code), qtt_iter=defs.QTT_ITERATION_GA, is_min=defs.IS_MINIMIZATION)
    return fn_factory


ALG_CLASS_NAME_DICT = {
    'SimpleHillClimbing': factory_simple_hillclimbing,
    'RestartHillClimbing': factory_restart_hillclimbing,
    'SimulatedAnnealing': factory_simulated_annealing,
    'GeneticAlgorithm': factory_genetic_algorithm   
}

def get_factory(alg_class_name, problem_number):
    defs = get_defs(problem_number)
    return ALG_CLASS_NAME_DICT[alg_class_name](defs)
