"""
Módulo para apresentação do gráfico por algoritmo e problema

"""
import numpy as np
import csv
import os.path
from matplotlib import pyplot as plt
import seaborn as sns; sns.set(style="darkgrid")
import pandas as pd
from run_to_csv import output_filepath, get_output_file

_algs = {'SimpleHillClimbing': "red", 'RestartHillClimbing': "green", 'SimulatedAnnealing': "blue", 'GeneticAlgorithm': "black"}
_problem_numbers = [1, 2, 3]
_exec_codes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def get_csv_files(alg, problem_number):
    files = []
    for ec in _exec_codes:
        files.append(get_output_file(alg, problem_number, ec, output_filepath))
    return files

def plot_performance(n_calls, mat_10_x_1000, mean, std, color):
    plt.plot(n_calls, mean, color=color) 
    plt.fill_between(n_calls, mean - std, mean + std, alpha=0.3, facecolor=color)
    
def plot_alg(alg_name, problem_number):
        csv_files = get_csv_files(alg_name, problem_number)
        dataset = []
        for file in csv_files:
            dataframe = pd.read_csv(file, usecols=["best_state_fitness"])
            array_1x1000 = dataframe['best_state_fitness'].to_numpy()
            dataset.append(adjust_data_to_plot(array_1x1000, 1000))
        mean = np.mean(dataset, axis=0)
        std = np.std(dataset, axis=0)
        plot_performance(range(1000), dataset, mean, std, _algs[alg_name])

def adjust_data_to_plot(result_exec, qtt):
    len_result = len(result_exec)
    if len_result == qtt:
        return result_exec
    else:
        adjusted_data = []
        qtt_extra = int(qtt / len_result)
        for iteration in result_exec:
            for i in range(0, qtt_extra):
                adjusted_data.append(iteration)
        return adjusted_data        


def show_comp(problem_number):
    for alg in _algs.keys():
        plot_alg(alg, problem_number)
    
    plt.title(f"Problema {problem_number}")
    plt.legend(_algs.keys())
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show()
        
if __name__ == '__main__':
    show_comp(problem_number=3)
    


