"""
Módulo para apresentação do gráfico por algoritmo e problema

"""
import numpy as np
import csv
import os.path
from matplotlib import pyplot as plt
import seaborn as sns; sns.set(style="darkgrid")
from run_to_csv import run_to_csv

_exec_codes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def plot_performance(n_calls, mat_1_x_1000):
    plt.plot(n_calls, mat_1_x_1000) 

def plot_chart(title, legend, result, qtt):
    plt.title(title)
    if result and result[0]:
        for i in range(0, len(result)):
            to_plot = adjust_data_to_plot(result[i], qtt)
            plot_performance(range(len(to_plot)), to_plot)
    plt.legend(legend)

def adjust_data_to_plot(result_exec, qtt):
    len_result = len(result_exec)
    if len_result == qtt:
        return list(map(lambda d: d['best_state_fitness'], result_exec))
    else:
        adjusted_data = []
        qtt_extra = int(qtt / len_result)
        for iteration in result_exec:
            for i in range(0, qtt_extra):
                adjusted_data.append(iteration['best_state_fitness'])
        return adjusted_data

output_filepath = 'c:/Temp/resultados/'
def run_to_chart(algorithm_name, problem_number=1, exec_codes=_exec_codes, show_chart=True, show_statistics=True, output_csvfile=None):

    result = run_to_csv(algorithm_name, problem_number, exec_codes, show_statistics=show_statistics, output_csvfile=output_filepath)
    data = result['data']

    if show_chart:
        legend = list(map(lambda e: f'Exec {e}', exec_codes))
        plot_chart(algorithm_name, legend, data, 1000)
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')
        plt.show()
    return result
    
if __name__ == '__main__':

    #run_to_chart("SimpleHillClimbing", problem_number=1)
    #run_to_chart("RestartHillClimbing", problem_number=1)
    #run_to_chart("SimulatedAnnealing", problem_number=1)
    #run_to_chart("GeneticAlgorithm", problem_number=1)

    #run_to_chart("SimpleHillClimbing", problem_number=2)
    #run_to_chart("RestartHillClimbing", problem_number=2)
    #run_to_chart("SimulatedAnnealing", problem_number=2)
    #run_to_chart("GeneticAlgorithm", problem_number=2)

    #run_to_chart("SimpleHillClimbing", problem_number=3)
    #run_to_chart("RestartHillClimbing", problem_number=3)
    #run_to_chart("SimulatedAnnealing", problem_number=3)
    run_to_chart("GeneticAlgorithm", problem_number=3)
