"""
Módulo execução de algoritmo X problema

"""
from factory import get_factory

_to_print = True

def execute(algorithm_name, problem_number=1, exec_codes=[1,2,3,4,5,6,7,8,9,10]):
    results = []
    for e in exec_codes:
        results.append(execute_one(algorithm_name, problem_number, e))
    return results


def execute_one(algorithm_name, problem_number=1, exec_code=1, to_print=_to_print):

    factory = get_factory(algorithm_name, problem_number)
    algorithm = factory(exec_code = exec_code)

    to_return = []
    if to_print: print(f'Starting for: {algorithm_name} to problem: {problem_number} execution: {exec_code}')
    for (neighbor, current, best) in algorithm:
            dict_csv = algorithm.to_dict()
            dict_csv['execution_code'] = f'{exec_code}'
            to_return.append(dict_csv)
    if to_print: print(f'Finished for: {algorithm_name} to problem: {problem_number} execution: {exec_code}. Best: {algorithm.best_state}')
    return to_return

if __name__ == '__main__':
    
    #result = execute_one("SimpleHillClimbing", problem_number=1, exec_code=5)
    result = execute("SimpleHillClimbing", problem_number=1, exec_codes=[1,2,3,4,5,6,7,8,9,10])

    #result = execute_one("RestartHillClimbing", problem_number=1, exec_code=5)
    #result = execute("RestartHillClimbing", problem_number=1, exec_codes=[1,2,3,4,5,6,7,8,9,10])

    #result = execute_one("SimulatedAnnealing", problem_number=1, exec_code=5)
    #result = execute("SimulatedAnnealing", problem_number=1, exec_codes=[1,2,3,4,5,6,7,8,9,10])

    #result = execute_one("GeneticAlgorithm", problem_number=1, exec_code=5)
    #result = execute("GeneticAlgorithm", problem_number=2, exec_codes=[1,2,3,4,5,6,7,8,9,10])
