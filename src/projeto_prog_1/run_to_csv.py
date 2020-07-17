"""
Módulo para execução e escrita de CSV por algoritmo e problema

"""
import numpy as np
import csv
import os.path
from matplotlib import pyplot as plt
import seaborn as sns; sns.set(style="darkgrid")
from runner import execute

_exec_codes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Header do CSV para todos os problemas
_csv_header = ['algorithm', 'execution_code', 'iteration', 'best_state_value', 'best_state_fitness']

def print_statistics(algorithm_name, results):
    data = []
    for r in results:
        data.append(list(map(lambda d: d['best_state_fitness'], r)))

    data_np = np.array(data)
    mini = np.amin(data_np)
    maxi = np.amax(data_np)
    mean = np.mean(data_np)
    std = np.std(data_np)

    print(f'{algorithm_name}|{maxi}|{mini}|{mean}|{std}')

def get_output_file(alg_name, problem_number, exec_code, file_path):
    return f'{file_path}p{problem_number}_{alg_name}_{exec_code}.csv'

def gen_output_csv(output_file, header):
    if not os.path.exists(output_file):
        with open(output_file, mode='w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()    
    else:
        os.remove(output_file)
        with open(output_file, mode='w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()
            
def write_csv(data, output_file):
    with open(output_file, mode='a', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=_csv_header)
        for record in data:
            csv_writer.writerow(record)            

def save_csv(algorithm_name, problem_number, result, output_path):
    files = []
    for i in range(0, len(result)):
        output_file = get_output_file(algorithm_name, problem_number, i + 1, output_path)
        gen_output_csv(output_file, _csv_header)
        write_csv(result[i], output_file)
        files.append(output_file)
    return files


def run_to_csv(algorithm_name, problem_number=1, exec_codes=_exec_codes, show_statistics=True, output_csvfile=None):
    result = execute(algorithm_name, problem_number, exec_codes)
    if show_statistics: print_statistics(algorithm_name, result)
    files = save_csv(algorithm_name, problem_number, result, output_csvfile) if output_csvfile else None
    return {'data': result, 'csv_files':files}


output_filepath = 'c:/Temp/resultados/'
    
if __name__ == '__main__':
    result = run_to_csv("SimpleHillClimbing", problem_number=1, output_csvfile=output_filepath)
    #result = run_to_csv("RestartHillClimbing", problem_number=1, output_csvfile=output_filepath)
    #result = run_to_csv("SimulatedAnnealing", problem_number=1, output_csvfile=output_filepath)
    #result = run_to_csv("GeneticAlgorithm", problem_number=1, output_csvfile=output_filepath)

    #result = run_to_csv("SimpleHillClimbing", problem_number=2, output_csvfile=output_filepath)
    #result = run_to_csv("RestartHillClimbing", problem_number=2, output_csvfile=output_filepath)
    #result = run_to_csv("SimulatedAnnealing", problem_number=2, output_csvfile=output_filepath)
    #result = run_to_csv("GeneticAlgorithm", problem_number=2, output_csvfile=output_filepath)

    #result = run_to_csv("SimpleHillClimbing", problem_number=3, output_csvfile=output_filepath)
    #result = run_to_csv("RestartHillClimbing", problem_number=3, output_csvfile=output_filepath)
    #result = run_to_csv("SimulatedAnnealing", problem_number=3, output_csvfile=output_filepath)
    #result = run_to_csv("GeneticAlgorithm", problem_number=3, output_csvfile=output_filepath)
